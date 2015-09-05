import re

from django.utils import six
from rest_framework import serializers

from .models import FieldsMap, County, District, School, Record


class FormattedCharField(serializers.CharField):
    def to_internal_value(self, data):
        value = six.text_type(data).title()
        return value.strip() if self.trim_whitespace else value


class CapitalizedCharField(serializers.CharField):
    def to_internal_value(self, data):
        value = six.text_type(data).upper()
        return value.strip() if self.trim_whitespace else value


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


class CdeSchoolModeField(SchoolTypeField):
    def to_internal_value(self, data):
        return (
            '1'
            if super(CdeSchoolModeField, self).to_internal_value(data)
            else '3'
        )


class CdeSchoolSearchInput(serializers.Serializer):
    code = serializers.CharField(source='cds_code')
    city = FormattedCharField()
    public = CdeSchoolModeField(source='mode')
    status = serializers.CharField(max_length=1)


class CdssFacilitySearchInput(serializers.Serializer):
    code = serializers.CharField(source='facnum')


class FieldsMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldsMap
        exclude = ('id', 'dataset',)


class CountySerializer(serializers.ModelSerializer):
    county = FormattedCharField(source='name')

    class Meta:
        model = County
        fields = ('county',)


class DistrictSerializer(serializers.ModelSerializer):
    district = FormattedCharField(source='name')

    class Meta:
        model = District
        fields = ('district',)


class SchoolSerializer(serializers.ModelSerializer):
    name = FormattedCharField()
    address = CapitalizedCharField()
    city = FormattedCharField()
    public = SchoolTypeField(default=False)

    class Meta:
        model = School
        exclude = ('county', 'district',)


class RecordSerializer(serializers.ModelSerializer):
    reported = ReportedField(default=False)

    class Meta:
        model = Record
        exclude = ('dataset', 'school',)
