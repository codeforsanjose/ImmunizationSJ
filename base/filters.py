from django.db import models

import django_filters


class BaseFilterSet(django_filters.FilterSet):
    filter_lookup_types = {
        django_filters.CharFilter: 'icontains',
    }

    def __init__(self, *args, **kwargs):
        super(BaseFilterSet, self).__init__(*args, **kwargs)
        self._apply_filter_lookup_types()

    def _apply_filter_lookup_types(self):
        if not self.filter_lookup_types:
            return

        for f in self.filters:
            f_type = self.filters[f].__class__
            if f_type in self.filter_lookup_types:
                self.filters[f].lookup_type = self.filter_lookup_types[f_type]
