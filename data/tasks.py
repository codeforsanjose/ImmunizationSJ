import re

from celery import shared_task

from django.db import transaction
from django.utils import timezone

from .cdph.api import CdphViews, CdphMigrations
from .models import Dataset
from .serializers import FieldsMapSerializer

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

        # Custom value transformations
        # 'public' must be a boolean field
        data['public'] = data['public'].lower() == 'public',

        # 'reported' must be a boolean field
        data['reported'] = data['reported'].lower() in ('y', 'yes')

        print data

    # Update dataset entry to reflect successful import
    dataset.sourced = True
    dataset.save()

@shared_task
def source_datasets():
    for d in Dataset.objects.all():
        try:
            # Commit each dataset as a whole
            with transaction.atomic():
                source_dataset(d)
        except:
            # Add logging here
            continue


