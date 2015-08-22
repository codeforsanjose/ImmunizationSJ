from rest_framework import serializers

from data.models import Dataset, County, District, School, Record, Summary


class DatasetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Dataset


class CountySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = County


class DistrictSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = District


class SchoolSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = School


class RecordListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Record


class RecordDetailSerializer(serializers.HyperlinkedModelSerializer):
    county_summary = serializers.ReadOnlyField()
    district_summary = serializers.ReadOnlyField()

    class Meta:
        model = Record


class SummaryListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Summary
        fields = ('url', 'dataset',)


class SummaryDetailSerializer(serializers.HyperlinkedModelSerializer):
    summary = serializers.ReadOnlyField()

    class Meta:
        model = Summary
        exclude = ('sector',)
