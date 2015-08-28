import requests
import xmltodict

BASE_API_URL = 'https://cdph.data.ca.gov/'


class CdphError(Exception):
    pass


class CdphAPI(object):
    endpoint = None

    def __init__(self):
        super(CdphAPI, self).__init__()

    def _api_call(self, uid):
        return BASE_API_URL + self.endpoint.format(uid=uid)

    def _request(self, uid):
        response = requests.get(self._api_call(uid))
        if response.status_code != requests.codes.ok:
            raise CdphError(
                'ERROR: {status} {message}'.format(status=response.status_code,
                                                   message=response.reason)
            )

        return response


class CdphViews(CdphAPI):
    endpoint = 'resource/{uid}.json?$limit=50000'

    def get_content(self, uid):
        response = self._request(uid)
        return response.json()


class CdphMigrations(CdphAPI):
    endpoint = 'api/migrations/{uid}.json'

    def _next_update(self, uid):
        response = self._request(uid)
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
