from rest_framework import serializers

from .models import FieldsMap, Record


class FieldsMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldsMap
        exclude = ('id', 'dataset',)


class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        exclude = ('dataset',)
