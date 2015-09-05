from .cdss import CdssFacilitySearch
from .cde import CdeSchoolSearch

# Constants for types of schools
TYPE_PUBLIC = 'PUBLIC'
TYPE_PRIVATE = 'PRIVATE'


class ChildCareFacilitySearch(CdssFacilitySearch):
    def __init__(self):
        super(ChildCareFacilitySearch, self).__init__()
        self.cde = CdeSchoolSearch()

    def get_search_results(self, **field_values):
        result = (
            super(ChildCareFacilitySearch, self)
            .get_search_results(**field_values)
        )
        if result:
            return result

        # Try to perform public and private searches using
        # the CDE database if above fails to return a result
        for school_type in (TYPE_PUBLIC, TYPE_PRIVATE,):
            field_update = {'public': school_type}

            # Inject in school type for search
            field_values.update(field_update)

            result = self.cde.get_search_results(**field_values)
            if result:
                # If result exists for specified school type, update.
                result.update(field_update)
                return result
