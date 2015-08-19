import re

from celery import shared_task

from django.db import transaction
from django.utils import timezone

from .cdph.api import CdphViews, CdphMigrations
from .models import (Dataset, Sector, City, County,
                     District, School, Record, Summary)
from .serializers import (FieldsMapSerializer, CitySerializer,
                          CountySerializer, DistrictSerializer,
                          SchoolSerializer, RecordSerializer)

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
    if dataset.sourced:
        return

    # Build dataset-specific mappings for field names
    mappings = get_field_mappings(dataset.fields_map)

    for entry in CdphViews().get_content(dataset.uid):
        # Apply field name mappings
        data = {mappings.get(k, k): v for k, v in entry.iteritems() if v}

        # Create required sectors
        # Create city
        city_serializer = CitySerializer(data=data)
        city_serializer.is_valid(raise_exception=True)
        city, _ = City.objects.get_or_create(
            **city_serializer.validated_data)

        # Create county
        county_serializer = CountySerializer(data=data)
        county_serializer.is_valid(raise_exception=True)
        county, _ = County.objects.get_or_create(
            **county_serializer.validated_data)

        # Create school
        school_serializer = SchoolSerializer(data=data)
        school_serializer.is_valid(raise_exception=True)
        school, _ = School.objects.update_or_create(
            defaults=school_serializer.validated_data,
            code=school_serializer.validated_data['code'],
            city=city,
            county=county
        )

        # Add district to school if it exists:
        district_serializer = DistrictSerializer(data=data)
        # No need to raise exception here since this is an optional field
        if district_serializer.is_valid():
            school.district, _ = District.objects.get_or_create(
                **district_serializer.validated_data)
            school.save()

        ## Finally create record
        record_serializer = RecordSerializer(data=data)
        record_serializer.is_valid(raise_exception=True)
        Record.objects.update_or_create(
            defaults=record_serializer.validated_data,
            dataset=dataset,
            school=school
        )

def cache_summary(dataset, sector):
    records = Record.objects.filter(dataset=dataset).filter(school__in=sector.schools.all())
    # Do something with records
    Summary.objects.update_or_create(defaults={'summary': ''},
                                     dataset=dataset,
                                     sector=sector.sector_ptr,
                                     summary_type='ALL')

def cache_summaries(dataset):
    try:
        for _Sector in (City, County, District,):
            for sector in _Sector.objects.all():
                cache_summary(dataset, sector)
    except:
        # Add logging here
        raise

@shared_task
def source_datasets():
    for d in Dataset.objects.all():
        try:
            # Commit each dataset as a whole
            with transaction.atomic():
                source_dataset(d)
                cache_summaries(d)
                d.sourced = True
                d.save()
        except:
            # Add logging here
            raise
