from rest_framework.routers import DefaultRouter

from .views import (
    DatasetViewSet,
    CountyViewSet,
    DistrictViewSet,
    SchoolViewSet,
    RecordViewSet,
    SummaryViewSet
)

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'datasets', DatasetViewSet)
router.register(r'counties', CountyViewSet)
router.register(r'districts', DistrictViewSet)
router.register(r'schools', SchoolViewSet)
router.register(r'records', RecordViewSet)
router.register(r'summaries', SummaryViewSet)
