import json
from typing import Optional, List
import requests
from l9format import l9format
from enum import Enum
from serde import Model, fields
from leakix.response import SuccessResponse, ErrorResponse, RateLimitResponse
from leakix.query import *
from leakix.plugin import *
from leakix.plugin import APIResult
from leakix.field import *


__VERSION__ = "0.1.8"


class Scope(Enum):
    SERVICE = "service"
    LEAK = "leak"


class HostResult(Model):
    Services: fields.Optional(fields.List(fields.Nested(l9format.L9Event)))
    Leaks: fields.Optional(fields.List(fields.Nested(l9format.L9Event)))


DEFAULT_URL = "https://leakix.net"


class Client:
    MAX_RESULTS_PER_PAGE = 20

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = DEFAULT_URL,
    ):
        self.api_key = api_key
        self.base_url = base_url if base_url else DEFAULT_URL
        self.headers = {
            "Accept": "application/json",
            "User-agent": "leakix-client-python/%s" % __VERSION__,
        }
        if api_key:
            self.headers["api-key"] = api_key

    def __get(self, url, params):
        r = requests.get(
            url,
            params=params,
            headers=self.headers,
        )
        if r.status_code == 200:
            response_json = r.json() if r.content else []
            return SuccessResponse(response=r, response_json=response_json)
        elif r.status_code == 429:
            return RateLimitResponse(response=r)
        elif r.status_code == 204:
            return ErrorResponse(response=r, response_json=[], status_code=200)
        else:
            return ErrorResponse(response=r, response_json=r.json())

    def get(self, scope: Scope, queries: Optional[List[Query]] = None, page: int = 0):
        """
        The function takes a scope (either "leaks" or "services"). The value can be constructed using `Scope.SERVICE` or
        `Scope.LEAK`.
        The second parameter is a list of queries. The default value will be considered as the wildcard `*`, which is
        also the default value on the web interface.
        Structured queries can be built using the different classes in `query.py` and `field.py`.
        If you want to build "raw" queries, like on the search bar on the website, use the class `RawQuery`.

        The output will be an abstract response, which can be a successfull HTTP response (represented by the class
        `SuccessResponse`) or a failed HTTP response (represented by the class `ErrorResponse`).
        Methods `is_success` and `is_error` are provided to the user to verify in their application what the state of
        the response is.

        The output of a query can be accessed using the method `json`, for instance `response.json()`.
        In the case of a successfull response, the output will be a list of L9Event.
        When you have an object of type `l9Event` (or the longer
        `l9format.l9format.L9Event`), you can refer to
        [L9Event](https://github.com/LeakIX/l9format-python/blob/main/l9format/l9format.py#L158)
        model class for the available fields.
        For instance, to access the IP of an object `event` of type `L9Event`, you can
        use `event.ip`.
        """
        if page < 0:
            raise ValueError("Page argument must be a positive integer")
        if queries is None or len(queries) == 0:
            serialized_query = EmptyQuery().serialize()
        else:
            serialized_query = [q.serialize() for q in queries]
            serialized_query = " ".join(serialized_query)
            serialized_query = "%s" % serialized_query
        url = "%s/search" % self.base_url
        r = self.__get(
            url=url, params={"scope": scope.value, "q": serialized_query, "page": page}
        )
        return r

    def get_service(self, queries: Optional[List[Query]] = None, page: int = 0):
        """
        Shortcut for `get` with the scope `Scope.Service`.

        """
        r = self.get(Scope.SERVICE, queries=queries, page=page)
        if r.is_success():
            r.response_json = [
                l9format.L9Event.from_dict(res) for res in r.response_json
            ]
        return r

    def get_leak(self, queries: Optional[List[Query]] = None, page: int = 0):
        """
        Shortcut for `get` with the scope `Scope.Leak`.
        """
        r = self.get(Scope.LEAK, queries=queries, page=page)
        if r.is_success():
            r.response_json = [
                l9format.L9Event.from_dict(res) for res in r.response_json
            ]
        return r

    def get_host(self, ipv4: str):
        """
        Returns the list of services and associated leaks for a given host. Only the ipv4 format is supported at the
        moment.
        """
        url = "%s/host/%s" % (self.base_url, ipv4)
        r = self.__get(url, params=None)
        if r.is_success():
            response_json = r.json()
            formatted_result = HostResult.from_dict(response_json)
            response_json = {
                "services": formatted_result.Services,
                "leaks": formatted_result.Leaks,
            }
            r.response_json = response_json
        return r

    def get_plugins(self):
        """
        Returns the list of plugins the authenticated user with the given API key has access to.

        The output is a list of `APIResult` objects. The fields are `name` which is the plugin name, and `description`
        which contains a brief description of the plugin.
        Paid users have access to a broader list of plugins. The full list you can be found on
        https://leakix.net/plugins.
        For the paid plans, have a look at https://leakix.net/plans.
        """
        url = "%s/api/plugins" % (self.base_url)
        r = self.__get(url, params=None)
        if r.is_success():
            r.response_json = [APIResult.from_dict(d) for d in r.json()]
        return r

    def bulk_export(self, queries: Optional[List[Query]] = None):
        url = "%s/bulk/search" % (self.base_url)
        if queries is None or len(queries) == 0:
            serialized_query = EmptyQuery().serialize()
        else:
            serialized_query = [q.serialize() for q in queries]
            serialized_query = " ".join(serialized_query)
            serialized_query = "%s" % serialized_query
        params = {"q": serialized_query}
        r = requests.get(url, params=params, headers=self.headers, stream=True)
        if r.status_code == 200:
            response_json = []
            for line in r.iter_lines():
                json_event = json.loads(line)
                response_json.append(l9format.L9Aggregation.from_dict(json_event))
            return SuccessResponse(response=r, response_json=response_json)
        elif r.status_code == 429:
            return RateLimitResponse(response=r)
        elif r.status_code == 204:
            return ErrorResponse(response=r, response_json=[], status_code=200)
        else:
            return ErrorResponse(response=r, response_json=r.json())
        return r
