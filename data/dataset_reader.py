from django.db import transaction
from django.utils import timezone
from geopy.geocoders import GoogleV3

from .api.cdph import CdphViews, CdphMigrations
from .api.cde import CdeSchoolSearch
from .api.cc import ChildCareFacilitySearch
from .models import (
    Dataset,
    Sector,
    County,
    District,
    School,
    StatFieldsMixin,
    Record,
    Summary
)
from .serializers import (
    FieldsMapSerializer,
    CountySerializer,
    DistrictSerializer,
    SchoolSerializer,
    RecordSerializer
)

__SECTOR_TYPES__ = [
    i.related_model
    for i in Sector._meta.get_all_related_objects()
    if i.parent_link
]
__SUMMARIZE_FIELDS__ = [i.name for i in StatFieldsMixin._meta.fields]


class DatasetReader(object):
    def __init__(self, dataset):
        super(DatasetReader, self).__init__()
        self._dataset = dataset
        self._search_form = (
            ChildCareFacilitySearch()
            if self._dataset.grade == 'CC'
            else CdeSchoolSearch()
        )
        self.geocoder = GoogleV3()

    @staticmethod
    def _update_data(data, **kwargs):
        data.update(kwargs)

    @property
    def _latest(self):
        return CdphMigrations().get_latest_dataset(self._dataset.uid)

    @property
    def _raw(self):
        return CdphViews().get_content(self._dataset.uid)

    @property
    def _field_mappings(self):
        return {
            v: k
            for k, v in
                FieldsMapSerializer(self._dataset.fields_map).data.iteritems()
            if v
        }

    def _update(self):
        uid, updated = self._latest
        if updated:
            self._dataset.uid = uid
            self._dataset.queued_date = timezone.now()
            self._dataset.sourced = False
            self._dataset.save()

    def _source(self):
        if self._dataset.sourced:
            return

        # Build dataset-specific mappings for field names
        mappings = self._field_mappings

        for entry in self._raw:
            # Apply field name mappings
            data = {mappings.get(k, k): v for k, v in entry.iteritems() if v}

            # Extract school information and update raw data
            if not self._update_school_info(data):
                continue

            # Create the necessary model instances from the data dict
            self._serialize_to_objects(data)

        self._cache_summaries()
        self._dataset.sourced = True
        self._dataset.save()

    def _update_school_info(self, data):
        info = self._search_form.get_search_results(**data)
        if not info:
            # Log invalid school
            return False

        address = info.get('address', None)
        # Extract latitude and longitude for address
        geolocation = self.geocoder.geocode(address)
        self._update_data(data,
                          latitude=getattr(geolocation, 'latitude', None),
                          longitude=getattr(geolocation, 'longitude', None),
                          **info)
        return True

    def _serialize_to_objects(self, data):
        # Create county
        county_serializer = CountySerializer(data=data)
        county_serializer.is_valid(raise_exception=True)
        county, _ = County.objects.get_or_create(
            **county_serializer.validated_data)

        # Create school in the above county
        school_serializer = SchoolSerializer(data=data)
        school_serializer.is_valid(raise_exception=True)
        school, _ = School.objects.update_or_create(
            defaults=school_serializer.validated_data,
            code=school_serializer.validated_data['code'],
            county=county
        )

        # Create a district as well, if possible
        district_serializer = DistrictSerializer(data=data)
        # No need to raise exception here since this is an optional field
        if district_serializer.is_valid():
            district, _ = District.objects.get_or_create(
                county=county,
                **district_serializer.validated_data
            )
            # Save district to school
            school.district = district
            school.save()

        ## Finally create record
        record_serializer = RecordSerializer(data=data)
        record_serializer.is_valid(raise_exception=True)
        Record.objects.update_or_create(
            defaults=record_serializer.validated_data,
            dataset=self._dataset,
            school=school
        )

    def _cache_summaries(self):
        for _Sector in __SECTOR_TYPES__:
            for sector in _Sector.objects.all():
                summary = self._generate_summary(sector)
                Summary.objects.update_or_create(defaults={'summary': summary},
                                                 dataset=self._dataset,
                                                 sector=sector.sector_ptr)

    def _generate_summary(self, sector):
        records = (
            Record.objects
            .filter(dataset=self._dataset)
            .filter(reported=True)
            .filter(school__in=sector.schools.all())
        )
        # Only use reported values for calculating summaries
        records_df = (
            records
            .to_dataframe(__SUMMARIZE_FIELDS__)
            .dropna(axis=1, how='all')
        )
        by = [
            'public' if is_public else 'private'
            for is_public in records.values_list('school__public', flat=True)
        ]

        if not records_df.empty:
            return self._format_summary(('all', records_df),
                                        *records_df.groupby(by))

    def _format_summary(self, *args):
        return {
            k: self._summarize_df(v)
            for k, v in args
        }

    def _summarize_df(self, df):
        # All pandas-friendly summarizations go here.
        return df.describe().to_dict()

    def to_db(self):
        try:
            self._update()

            # Commit each dataset as a whole
            with transaction.atomic():
                self._source()
        except:
            # Add logging here
            pass
