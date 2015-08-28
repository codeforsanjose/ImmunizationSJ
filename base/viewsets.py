from rest_framework import mixins
from rest_framework import viewsets


class RetrieveOnlyModelViewSet(mixins.RetrieveModelMixin,
                               viewsets.GenericViewSet):
    pass
