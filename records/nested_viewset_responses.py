from base.nested_viewset_responses import NestedViewSetList

from data.models import District, School, Record, Summary

from .serializers import (
    DistrictSerializer,
    SchoolSerializer,
    RecordListSerializer,
    SummaryListSerializer
)
from .filters import DistrictFilter, SchoolFilter, RecordFilter, SummaryFilter


class NestedViewSetDistrictList(NestedViewSetList):
    model = District
    serializer_class = DistrictSerializer
    filter_class = DistrictFilter


class NestedViewSetSchoolList(NestedViewSetList):
    model = School
    serializer_class = SchoolSerializer
    filter_class = SchoolFilter


class NestedViewSetRecordList(NestedViewSetList):
    model = Record
    serializer_class = RecordListSerializer
    filter_class = RecordFilter


class NestedViewSetSummaryList(NestedViewSetList):
    model = Summary
    serializer_class = SummaryListSerializer
    filter_class = SummaryFilter
