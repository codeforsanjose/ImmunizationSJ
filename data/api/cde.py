from lxml import html
from .generics import ExternalAPI, SearchFormMixin, SearchResult
from .serializers import CdeSchoolSearchInput
from .decorators import field


class CdeAPI(ExternalAPI):
    base_url = 'http://www.cde.ca.gov/re/sd/'


class CdeSchoolSearchResult(SearchResult):
    def parse_details_from_raw(self, raw):
        table = html.fromstring(raw).xpath(
            '//table[@class="table table-bordered"]'
            '/tr[th/@class="shadow details-field-label" and td]'
        )

        return {i.findtext('th/b'): i.find('td') for i in table}

    @field
    def phone(self):
        return self._details['Phone Number'].text

    @field
    def name(self):
        return self._details['School'].text

    @field
    def code(self):
        return self._details['CDS Code'].text.replace(' ', '')

    @field
    def county(self):
        return self._details['County'].text

    @field
    def district(self):
        return self._details['District'].findtext('a')

    @field
    def address(self):
        elem = self._details['School Address']

        # Remove the link to Yahoo Map if it exists
        map_link = elem.find('a')
        if map_link is not None:
            elem.remove(map_link)

        return ', '.join(elem.itertext())


class CdeSchoolSearch(SearchFormMixin, CdeAPI):
    endpoint = 'index.asp'
    form_id = 'search'
    form_timeout = 600 #10 minutes
    input_serializer_class = CdeSchoolSearchInput

    def get_search_results(self, **field_values):
        # Get and update the form
        form, form_page = self.get_form()
        self.update_form(form, field_values)

        # Finally submit the form
        submit = self.request(
            form.action,
            method='POST',
            headers={'Cookie': form_page.headers.get('set-cookie', None)},
            data=dict(form.form_values())
        )
        return CdeSchoolSearchResult(submit.text).to_dict()
