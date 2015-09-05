from lxml import html
from data.serializers import CdssFacilitySearchInput
from .generics import ExternalAPI, SearchFormMixin, SearchResult
from .decorators import field


class CdssAPI(ExternalAPI):
    base_url = 'https://secure.dss.ca.gov/'


class CdssFacilitySearchResult(SearchResult):
    def parse_details_from_raw(self, raw):
        return html.parse(raw).getroot().xpath(
            '//div[@class="container_style_b" and h4/text()="Facility Detail"]'
            '/div/table/tr'
        )

    def _get_element_by_key(self, lookup, text):
        for idx, elem in enumerate(self._details):
            for sub_idx, sub_elem in enumerate(elem.iterfind(lookup)):
                if sub_elem.text == text:
                    return idx, sub_idx, elem, sub_elem

    @field
    def name(self):
        return self._details[0].findtext('td')

    @field
    def address(self):
        # Address should span the next two lines after 'Address:'
        idx, _, _, _ = self._get_element_by_key('td', 'Address:')
        return ', '.join(
            self._details[i].findtext('td')
            for i in (idx+1, idx+2,)
        )

    @field
    def phone(self):
        _, _, _, elem = self._get_element_by_key('td', 'Phone:')
        return elem.getnext().text

    @field
    def code(self):
        _, _, _, elem = self._get_element_by_key('td', u'Facility\xa0Number:')
        return elem.getnext().text


class CdssFacilitySearch(SearchFormMixin, CdssAPI):
    endpoint = 'CareFacilitySearch/'
    form_id = 'searchinput'
    form_timeout = 3600 #1 hour
    input_serializer_class = CdssFacilitySearchInput

    def get_search_results(self, **field_values):
        # Get and update form
        form, _ = self.get_form()
        self.update_form(form, field_values)

        # Finally submit the form
        submit = html.submit_form(form)

        result = CdssFacilitySearchResult(submit)
        if result.is_valid():
            return result.to_dict()
