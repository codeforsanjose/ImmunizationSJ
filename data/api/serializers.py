from rest_framework import serializers


class CdeSchoolModeField(serializers.CharField):
    def to_internal_value(self, value):
        return '1' if value else '3'


class CdeSchoolSearchInput(serializers.Serializer):
    public = CdeSchoolModeField(source='mode')
    code = serializers.CharField(source='cds_code')
    city = serializers.CharField()


class CdssFacilitySearchInput(serializers.Serializer):
    code = serializers.CharField(source='facnum')
