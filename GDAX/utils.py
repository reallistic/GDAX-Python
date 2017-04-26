#
# GDAX/utils.py
# Michael Chase
#
# For utility functions and classes


class PaginatedList(list):
    def __init__(self, *args, **kwargs):
        self._client = kwargs.pop('client', None)
        self._nextPage = kwargs.pop('nextPageId', None)
        self._prevPage = kwargs.pop('prevPageId', None)
        list.__init__(self, *args, **kwargs)

    def setClient(self, client):
        self._client = client

    def setNextPage(self, pageId):
        self._nextPage = pageId

    def setPrevPage(self, pageId):
        self._prevPage = pageId

    def getNextPage(self):
        if self._client and self._nextPage:
            return self._client(nextPage=self._nextPage)
        return None

    def getPrevPage(self):
        if self._client and self._nextPage:
            return self._client(prevPage=self._prevPage)
        return None
