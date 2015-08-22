from celery import shared_task

from django.db import transaction
from django.utils import timezone

from .cdph.api import CdphViews, CdphMigrations
from .models import (Dataset, Sector, County, District,
                     School, Record, Summary)
from .serializers import (FieldsMapSerializer, CountySerializer,
                          DistrictSerializer, SchoolSerializer,
                          RecordSerializer)

_SUMM_FIELDS_ = ['up_to_date', 'conditional', 'pme', 'pbe', 'dtp',
                 'polio', 'mmr', 'hib', 'hepb', 'vari']

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

def source_dataset(dataset):
    # Build dataset-specific mappings for field names
    mappings = get_field_mappings(dataset.fields_map)

    for entry in CdphViews().get_content(dataset.uid):
        # Apply field name mappings
        data = {mappings.get(k, k): v for k, v in entry.iteritems() if v}

        # Create county
        county_serializer = CountySerializer(data=data)
        county_serializer.is_valid(raise_exception=True)
        county, _ = County.objects.get_or_create(
            **county_serializer.validated_data)

        # Create school in the above county
        school_serializer = SchoolSerializer(data=data)
        school_serializer.is_valid(raise_exception=True)
        school, _ = School.objects.get_or_create(
            defaults=school_serializer.validated_data,
            code=school_serializer.validated_data['code'],
            county=county
        )

        # Add district to school if it exists:
        district_serializer = DistrictSerializer(data=data)
        # No need to raise exception here since this is an optional field
        if district_serializer.is_valid():
            district, _ = District.objects.get_or_create(
                county=county,
                **district_serializer.validated_data
            )

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

def generate_summary(dataset, sector):
    records = (
        Record.objects
        .filter(dataset=dataset)
        .filter(reported=True)
        .filter(school__in=sector.schools.all())
    )

    records_df = records.to_dataframe(_SUMM_FIELDS_).dropna(axis=1, how='all')
    by = ['public' if is_public else 'private' for is_public in
          records.values_list('school__public', flat=True)]

    if not records_df.empty:
        summary = {is_public: subset.describe().to_dict()
                   for is_public, subset in records_df.groupby(by)}
        summary['all'] = records_df.describe().to_dict()
        return summary

def cache_summaries(dataset):
    for _Sector in (County, District,):
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
            raise
