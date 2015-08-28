from django.contrib import admin

from .models import Dataset, FieldsMap, School, Record


class FieldsMapInline(admin.StackedInline):
    model = FieldsMap


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ('year', 'grade', 'uid', 'queued_date', 'sourced',)
    inlines = (FieldsMapInline,)
