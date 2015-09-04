from .generics import ExternalAPI


class CdphAPI(ExternalAPI):
    base_url = 'https://cdph.data.ca.gov/'


class CdphViews(CdphAPI):
    endpoint = 'resource/{uid}.json?$limit=50000'

    def get_content(self, uid):
        response = self.request(uid=uid)
        return response.json()


class CdphMigrations(CdphAPI):
    endpoint = 'api/migrations/{uid}.json'

    def _next_update(self, uid):
        response = self.request(uid=uid)
        json = response.json()
        return json.get('nbeId', None)

    def get_latest_dataset(self, uid):
        updated = False
        while True:
            update = self._next_update(uid)
            if update is None or update == uid:
                break
            # An update was found.
            uid = update
            updated = True

        return uid, updated
