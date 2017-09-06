import os
from itertools import count

import requests


class HubAPI:
    def __init__(self, hapikey):
        self.session = requests.Session()
        self.hapikey = hapikey

    def request(self, method, url, params=None, **kwargs):
        if params is None:
            params = {}
        if url.startswith('/'):
            url = 'https://api.hubapi.com' + url
        if 'https://api.hubapi.com' in url:
            if isinstance(params, dict):
                params['hapikey'] = self.hapikey
            else:
                params = list(params) + [('hapikey', self.hapikey)]
        response = self.session.request(method=method, url=url, params=params, **kwargs)
        response.raise_for_status()
        return response.json()

    def load_paged(self,
        url, params=None,
        *,
        results_key='results',
        offset_param='offset',
        offset_key='offset',
        limit_param='limit',
        requestor=None
    ):
        if requestor is None:
            requestor = self.request
        if params is None:
            params = {}
        limit = 100
        offset = 0
        n_results = 0
        for page in count(1):
            params.update(**{offset_param: offset, limit_param: limit})
            response = requestor(method='get', url=url, params=params)
            results = response.get(results_key, [])
            n_results += len(results)
            print('Loaded page {page} ({n} results)'.format(page=page, n=n_results))
            yield from results
            if not (response.get('hasMore') or response.get('has-more')):
                break
            offset = response[offset_key]


def get_api():
    return HubAPI(hapikey=os.environ['HAPIKEY'])
