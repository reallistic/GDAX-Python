#
# GDAX/PublicClient.py
# Daniel Paquin
#
# For public requests to the GDAX exchange

import requests
from functools import partial

from .utils import PaginatedList


class PublicClient(object):
    def __init__(self, api_url="https://api.gdax.com", product_id="BTC-USD",
                 timeout=None):
        self.url = api_url
        if api_url[-1] == "/":
            self.url = api_url[:-1]
        self.productId = product_id
        self.timeout = timeout

    def makeRequest(self, endpoint, params=None):
        response = requests.get(self.url + endpoint, timeout=self.timeout,
                                params=params)
        return response

    def paginatedRequest(self, endpoint, params=None, nextPage=None,
                         prevPage=None):
        if params is None:
            params = {}
        if nextPage:
            params['before'] = nextPage
        elif prevPage:
            params['after'] = prevPage

        response = self.makeRequest(endpoint, params=params)
        params.pop('before', None)
        params.pop('after', None)
        return self.paginateResponse(endpoint, response, params=params)

    def paginateResponse(self, endpoint, response, params=None):
        resp_json = response.json()
        nextPage = response.headers.get('CB-BEFORE')
        prevPage = response.headers.get('CB-AFTER')
        client = partial(self.paginatedRequest, endpoint, params)
        return PaginatedList(resp_json, client=client, nextPageId=nextPage,
                             prevPageId=prevPage)

    def getProducts(self):
        response = self.makeRequest('/products').json()
        return response.json()

    def getProductOrderBook(self, json=None, level=2, product=''):
        if isinstance(json, dict):
            product = json.get("product", product)
            level = json.get('level', level)
        productId = product or self.productId
        params = dict(level=str(level))
        response = self.makeRequest('/products/%s/book' % productId, params)
        return response.json()

    def getProductTicker(self, json=None, product=''):
        if isinstance(json, dict):
            product = json.get("product", product)
        productId = product or self.productId
        response = self.makeRequest('/products/%s/ticker' % productId)
        return response.json()

    def getProductTrades(self, json=None, product=''):
        if isinstance(json, dict):
            product = json.get("product", product)

        productId = product or self.productId
        return self.paginatedRequest('/products/%s/trades' % productId)

    def getProductHistoricRates(self, json=None, product='', start='', end='', granularity=''):
        params = {}
        if isinstance(json, dict):
            product = json.pop("product", product)
            params = json
        else:
            params["start"] = start
            params["end"] = end
            params["granularity"] = granularity
        productId = product or self.productId
        response = self.makeRequest('/products/%s/candles' % productId, params)
        return response.json()

    def getProduct24HrStats(self, json=None, product=''):
        if isinstance(json, dict):
            product = json.pop("product", product)
        productId = product or self.productId
        response = self.makeRequest('/products/%s/stats' % productId)
        return response.json()

    def getCurrencies(self):
        response = self.makeRequest('/currencies')
        return response.json()

    def getTime(self):
        response = self.makeRequest('/time')
        return response.json()
