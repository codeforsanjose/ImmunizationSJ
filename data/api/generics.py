import requests

from django.core.cache import cache
from lxml import html
from .errors import APIError


class ExternalAPI(object):
    base_url = None
    endpoint = None

    def get_base_url(self):
        assert self.base_url is not None, (
            '%r should either include a `base_url` attribute, '
            'or override the `get_base_url()` method.'
            % self.__class__.__name__
        )

        return self.base_url

    def get_endpoint(self):
        assert self.endpoint is not None, (
            '%r should either include a `endpoint` attribute, '
            'or override the `get_endpoint()` method.'
            % self.__class__.__name__
        )

        return self.endpoint

    def api_call(self, endpoint=None, **kwargs):
        return (
            self.get_base_url() +
            (endpoint or self.get_endpoint()).format(**kwargs)
        )

    def request(self,
                url=None,
                method='GET',
                params=None,
                data=None,
                headers=None,
                **kwargs):
        response = requests.request(method,
                                    url or self.api_call(**kwargs),
                                    params=params,
                                    data=data,
                                    headers=headers)
        if response.status_code != requests.codes.ok:
            raise APIError(
                'ERROR: {status} {message}'.format(status=response.status_code,
                                                   message=response.reason)
            )

        return response


class SearchFormMixin(object):
    form_id = None
    form_timeout = None
    input_serializer_class = None

    def _get_form_by_form_id(self, forms):
        for f in forms:
            if f.get('id') == self.get_form_id():
                return f

    def get_form_id(self):
        assert self.form_id is not None, (
            '%r should either include a `form_id` attribute, '
            'or override the `get_form_id()` method.'
            % self.__class__.__name__
        )

        return self.form_id

    def get_form(self):
        form_page = cache.get(self.__class__.__name__)
        if not form_page:
            form_page = self.request()
            cache.set(self.__class__.__name__, form_page, self.form_timeout)

        form = self._get_form_by_form_id(html.fromstring(form_page.text).forms)

        return form, form_page

    def get_input_serializer_class(self):
        assert self.input_serializer_class is not None, (
            '%r should either include a `input_serializer_class` attribute, '
            'or override the `get_input_serializer_class()` method.'
            % self.__class__.__name__
        )

        return self.input_serializer_class

    def update_form(self, form, field_values):
        # Update form action
        form.action = self.api_call(form.action)

        # Update form fields
        serializer = self.get_input_serializer_class()(data=field_values)
        serializer.is_valid(raise_exception=True)
        form.fields.update(serializer.validated_data)

    def get_search_results(self, **field_values):
        raise NotImplementedError(
            '%r should override the `get_search_results()` method.'
            % self.__class__.__name__
        )


class SearchResult(object):
    def __init__(self, raw):
        super(SearchResult, self).__init__()
        self._details = self.parse_details_from_raw(raw)

    def parse_details_from_raw(self, raw):
        raise NotImplementedError(
            '%r should override the `parse_details_from_raw()` method.'
            % self.__class__.__name__
        )

    def is_valid(self):
        return bool(self._details)

    def get_fields(self):
        for i in dir(self):
            attr = getattr(self, i)
            if hasattr(attr, '__field__'):
                yield i, attr()

    def to_dict(self):
        return dict(self.get_fields())
