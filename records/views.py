from rest_framework import viewsets
from rest_framework.decorators import detail_route

from base.viewsets import RetrieveOnlyModelViewSet

from data.models import Dataset, County, District, School, Record, Summary

from .serializers import (
    DatasetSerializer,
    CountySerializer,
    DistrictSerializer,
    SchoolSerializer,
    RecordCompactSerializer,
    RecordSerializer,
    SummarySerializer
)
from .filters import (
    DatasetFilter,
    CountyFilter,
    DistrictFilter,
    SchoolFilter,
    RecordFilter
)
from .nested_viewset_responses import (
    NestedViewSetDistrictList,
    NestedViewSetSchoolList,
    NestedViewSetRecordList,
    NestedViewSetSummaryList
)


class DatasetViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer
    filter_class = DatasetFilter

    @detail_route()
    def records(self, request, pk=None):
        return NestedViewSetRecordList(
            view=self,
            request=request,
            qs_filter={'dataset__pk': pk}
        ).response


class SectorViewSet(viewsets.ReadOnlyModelViewSet):
    @detail_route()
    def summaries(self, request, pk=None):
        return NestedViewSetSummaryList(
            view=self,
            request=request,
            qs_filter={'sector__pk': pk}
        ).response


class CountyViewSet(SectorViewSet):
    queryset = County.objects.all()
    serializer_class = CountySerializer
    filter_class = CountyFilter

    @detail_route()
    def districts(self, request, pk=None):
        return NestedViewSetDistrictList(
            view=self,
            request=request,
            qs_filter={'county__pk': pk}
        ).response

    @detail_route()
    def schools(self, request, pk=None):
        return NestedViewSetSchoolList(
            view=self,
            request=request,
            qs_filter={'county__pk': pk}
        ).response


class DistrictViewSet(SectorViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    filter_class = DistrictFilter

    @detail_route()
    def schools(self, request, pk=None):
        return NestedViewSetSchoolList(
            view=self,
            request=request,
            qs_filter={'district__pk': pk}
        ).response


class SchoolViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    filter_class = SchoolFilter

    @detail_route()
    def records(self, request, pk=None):
        return NestedViewSetRecordList(
            view=self,
            request=request,
            qs_filter={'school__pk': pk}
        ).response


class RecordViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Record.objects.all()
    filter_class = RecordFilter

    def get_serializer_class(self):
        return RecordCompactSerializer if self.action == 'list' else \
            RecordSerializer


class SummaryViewSet(RetrieveOnlyModelViewSet):
    queryset = Summary.objects.all()
    serializer_class = SummarySerializer
