from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import detail_route

from data.models import Dataset, County, District, School, Record

from .serializers import (DatasetSerializer,
                          CountySerializer,
                          DistrictSerializer,
                          SchoolSerializer,
                          RecordListSerializer,
                          RecordDetailSerializer)


class DatasetViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer

    @detail_route()
    def records(self, request, pk=None):
        queryset = Record.objects.filter(dataset__pk=pk)
        serializer = RecordListSerializer(self.paginate_queryset(queryset),
                                          context={'request':request},
                                          many=True)
        return self.get_paginated_response(serializer.data)


class CountyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = County.objects.all()
    serializer_class = CountySerializer


class DistrictViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer


class SchoolViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer


class RecordViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Record.objects.all()

    def get_serializer_class(self):
        return RecordListSerializer if self.action == 'list' else \
            RecordDetailSerializer
