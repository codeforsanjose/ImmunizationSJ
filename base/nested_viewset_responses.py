from rest_framework.settings import api_settings


class NestedViewSetList(object):
    model = None
    serializer_class = None

    filter_backends = api_settings.DEFAULT_FILTER_BACKENDS

    def __init__(self, view, request, qs_filter=None):
        super(NestedViewSetList, self).__init__()
        self.view = view
        self.request = request
        self.qs_filter = qs_filter or {}

    def get_queryset(self):
        assert self.model is not None, (
            '%r should include a `model` attribute.'
            % self.__class__.__name__
        )

        return self.model.objects.filter(**self.qs_filter)

    def get_serializer(self, queryset):
        serializer_class = self.get_serializer_class()
        return serializer_class(queryset,
                                context={'request': self.request},
                                many=True)

    def get_serializer_class(self):
        assert self.serializer_class is not None, (
            '%r should either include a `serializer_class` attribute, '
            'or override the `get_serializer_class()` method.'
            % self.__class__.__name__
        )

        return self.serializer_class

    def filtered_queryset(self):
        queryset = self.get_queryset()
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)

        return queryset

    @property
    def response(self):
        queryset = self.filtered_queryset()

        page = self.view.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page)
            return self.view.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset)
        return Response(serializer.data)
