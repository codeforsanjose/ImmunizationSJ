from rest_framework import serializers

from data.models import Dataset, County, District, School, Record, Summary


class DatasetGradeMixin(serializers.Serializer):
    grade = serializers.CharField(source='get_grade_display')


class DatasetCompactSerializer(DatasetGradeMixin,
                               serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Dataset
        fields = ('url', 'year', 'grade',)


class DatasetSerializer(DatasetGradeMixin,
                        serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Dataset


class DatasetCompactMixin(serializers.Serializer):
    dataset = DatasetCompactSerializer(read_only=True)


class CountySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = County


class CountyMixin(serializers.Serializer):
    county = CountySerializer(read_only=True)


class DistrictCompactSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = District
        exclude = ('county',)


class DistrictSerializer(CountyMixin,
                         serializers.HyperlinkedModelSerializer):
    class Meta:
        model = District


class DistrictCompactMixin(serializers.Serializer):
    district = DistrictCompactSerializer(read_only=True)


class SchoolCompactSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = School
        fields = ('url', 'code', 'name',)


class SchoolSerializer(DistrictCompactMixin,
                       CountyMixin,
                       serializers.HyperlinkedModelSerializer):
    class Meta:
        model = School


class SchoolCompactMixin(serializers.Serializer):
    school = SchoolCompactSerializer(read_only=True)


class SchoolDetailMixin(serializers.Serializer):
    school = SchoolSerializer(read_only=True)


class RecordCompactSerializer(SchoolCompactMixin,
                              DatasetCompactMixin,
                              serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Record
        fields = ('url', 'dataset', 'school', 'reported')


class RecordSerializer(SchoolDetailMixin,
                       DatasetCompactMixin,
                       serializers.HyperlinkedModelSerializer):
    county_summary = serializers.ReadOnlyField()
    district_summary = serializers.ReadOnlyField()

    class Meta:
        model = Record


class SummaryCompactSerializer(DatasetCompactMixin,
                               serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Summary
        exclude = ('sector', 'summary',)


class SummarySerializer(DatasetCompactMixin,
                        serializers.HyperlinkedModelSerializer):
    summary = serializers.ReadOnlyField()

    class Meta:
        model = Summary
        exclude = ('sector',)
