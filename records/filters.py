import django_filters

from data.models import Dataset, County, District, School, Record, Summary


class DatasetFilter(django_filters.FilterSet):
    class Meta:
        model = Dataset
        fields = ('year', 'grade',)


class CountyFilter(django_filters.FilterSet):
    class Meta:
        model = County
        fields = ('name',)


class DistrictFilter(django_filters.FilterSet):
    county = django_filters.CharFilter(name='county__name')

    class Meta:
        model = District
        fields = ('name', 'county',)


class SchoolFilter(django_filters.FilterSet):
    county = django_filters.CharFilter(name='county__name')
    district = django_filters.CharFilter(name='district__name')

    class Meta:
        model = School
        fields = ('code', 'name', 'county', 'public', 'district', 'city',)


class RecordFilter(django_filters.FilterSet):
    year = django_filters.NumberFilter(name='dataset__year')
    grade = django_filters.CharFilter(name='dataset__grade')
    school = django_filters.CharFilter(name='school__name')
    county = django_filters.CharFilter(name='school__county__name')
    district = django_filters.CharFilter(name='school__district__name')

    class Meta:
        model = Record
        fields = ('year', 'grade', 'school', 'county', 'district', 'reported',)


class SummaryFilter(django_filters.FilterSet):
    year = django_filters.NumberFilter(name='dataset__year')
    grade = django_filters.CharFilter(name='dataset__grade')
    sector = django_filters.CharFilter(name='sector__name')

    class Meta:
        model = Summary
        fields = ('year', 'grade', 'sector',)
