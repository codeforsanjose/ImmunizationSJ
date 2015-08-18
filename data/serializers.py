from rest_framework import serializers

from .models import FieldsMap


class FieldsMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldsMap
        exclude = ('id', 'dataset',)
