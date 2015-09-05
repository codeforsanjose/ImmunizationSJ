from celery import shared_task

from .dataset_reader import DatasetReader
from .models import Dataset

@shared_task
def update_db():
    for dataset in Dataset.objects.all():
        reader = DatasetReader(dataset)
        reader.to_db()
