from django.contrib import admin

from .models import Dataset, FieldsMap, Record


class FieldsMapInline(admin.StackedInline):
    model = FieldsMap


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ('year', 'grade', 'uid', 'queued_date', 'sourced')
    list_filter = ('year', 'grade',)
    inlines = (FieldsMapInline,)


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'public', 'city', 'county', 'district')
    list_filter = ('county', 'public', 'dataset')
    search_fields = ('code', 'name', 'city', 'county', 'district')
