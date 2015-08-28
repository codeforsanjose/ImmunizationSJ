from celery import shared_task

from django.db import transaction
from django.utils import timezone

from .cdph.api import CdphViews, CdphMigrations
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

@shared_task
def update_datasets():
    api = CdphMigrations()
    for d in Dataset.objects.all():
        try:
            uid, updated = api.get_latest_dataset(d.uid)
            if updated:
                d.uid = uid
                d.queued_date = timezone.now()
                d.sourced = False
                d.save()
        except:
            # Add logging here
            continue

def get_field_mappings(f):
    return {v: k for k, v in FieldsMapSerializer(f).data.iteritems() if v}

def serialize_to_objects(dataset, data):
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
        dataset=dataset,
        school=school
    )

def source_dataset(dataset):
    # Build dataset-specific mappings for field names
    mappings = get_field_mappings(dataset.fields_map)

    for entry in CdphViews().get_content(dataset.uid):
        # Apply field name mappings
        data = {mappings.get(k, k): v for k, v in entry.iteritems() if v}

        # Create the necessary model instances from the data dict
        serialize_to_objects(dataset, data)

def summarize_df(df):
    # All pandas-friendly summarizations go here.
    return df.describe().to_dict()

def format_summary(*args):
    return {k: summarize_df(v) for k, v in args}

def generate_summary(dataset, sector):
    records = (
        Record.objects
        .filter(dataset=dataset)
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
        return format_summary(('all', records_df), *records_df.groupby(by))

def cache_summaries(dataset):
    for _Sector in __SECTOR_TYPES__:
        for sector in _Sector.objects.all():
            summary = generate_summary(dataset, sector)
            Summary.objects.update_or_create(defaults={'summary': summary},
                                             dataset=dataset,
                                             sector=sector.sector_ptr)

@shared_task
def update_db():
    for d in Dataset.objects.all():
        try:
            # Commit each dataset as a whole
            with transaction.atomic():
                if d.sourced:
                    continue

                source_dataset(d)
                cache_summaries(d)

                d.sourced = True
                d.save()
        except:
            # Add logging here
            continue
