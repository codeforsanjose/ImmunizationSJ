from base.nested_viewset_responses import NestedViewSetList

from data.models import District, School, Record, Summary

from .serializers import (
    DistrictCompactSerializer,
    SchoolCompactSerializer,
    RecordCompactSerializer,
    SummaryCompactSerializer
)
from .filters import DistrictFilter, SchoolFilter, RecordFilter, SummaryFilter


class NestedViewSetDistrictList(NestedViewSetList):
    model = District
    serializer_class = DistrictCompactSerializer
    filter_class = DistrictFilter


class NestedViewSetSchoolList(NestedViewSetList):
    model = School
    serializer_class = SchoolCompactSerializer
    filter_class = SchoolFilter


class NestedViewSetRecordList(NestedViewSetList):
    model = Record
    serializer_class = RecordCompactSerializer
    filter_class = RecordFilter


class NestedViewSetSummaryList(NestedViewSetList):
    model = Summary
    serializer_class = SummaryCompactSerializer
    filter_class = SummaryFilter
