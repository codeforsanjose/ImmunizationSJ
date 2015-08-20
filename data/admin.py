from django.contrib import admin

from .models import Dataset, FieldsMap, School, Record


class FieldsMapInline(admin.StackedInline):
    model = FieldsMap


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ('year', 'grade', 'uid', 'queued_date', 'sourced')
    inlines = (FieldsMapInline,)


class RecordInline(admin.TabularInline):
    model = Record


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'public', 'city', 'county', 'district')
    list_filter = ('public', 'county',)
    search_fields = ('code', 'name', 'city__name',
                     'county__name', 'district__name')
    inlines = (RecordInline,)
