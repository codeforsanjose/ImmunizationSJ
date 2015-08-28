import re

from rest_framework import serializers

from .models import FieldsMap, County, District, School, Record


class LazyBooleanField(serializers.BooleanField):
    TRUE_CASE_INSENSITIVE_REGEX = r''

    def to_internal_value(self, data):
        return (
            data in self.TRUE_VALUES or
            re.match(self.TRUE_CASE_INSENSITIVE_REGEX,
                     data,
                     re.IGNORECASE) is not None
        )

    def to_representation(self, value):
        return self.to_internal_value(value)


class SchoolTypeField(LazyBooleanField):
    TRUE_CASE_INSENSITIVE_REGEX = r'public'


class ReportedField(LazyBooleanField):
    TRUE_CASE_INSENSITIVE_REGEX = r'(y|yes)'


class FieldsMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldsMap
        exclude = ('id', 'dataset',)


class CountySerializer(serializers.ModelSerializer):
    county = serializers.CharField(source='name')

    class Meta:
        model = County
        fields = ('county',)


class DistrictSerializer(serializers.ModelSerializer):
    district = serializers.CharField(source='name')

    class Meta:
        model = District
        fields = ('district',)


class SchoolSerializer(serializers.ModelSerializer):
    public = SchoolTypeField(default=False)

    class Meta:
        model = School
        exclude = ('county', 'district',)


class RecordSerializer(serializers.ModelSerializer):
    reported = ReportedField(default=False)

    class Meta:
        model = Record
        exclude = ('dataset', 'school',)
