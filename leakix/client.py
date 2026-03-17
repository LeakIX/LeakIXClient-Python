import json
from enum import Enum
from typing import Any

import requests
from l9format import l9format

from leakix.base import BaseClient
from leakix.base import HostResult as HostResult
from leakix.query import AbstractQuery, serialize_queries
from leakix.response import (
    AbstractResponse,
    ErrorResponse,
    RateLimitResponse,
    SuccessResponse,
)


class Scope(Enum):
    SERVICE = "service"
    LEAK = "leak"


class Client(BaseClient):
    def __get(self, url: str, params: dict[str, Any] | None) -> AbstractResponse:
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

    def get(
        self,
        scope: Scope,
        queries: list[AbstractQuery] | None = None,
        page: int = 0,
    ) -> AbstractResponse:
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
        serialized_query = serialize_queries(queries)
        url = f"{self.base_url}/search"
        return self.__get(
            url=url,
            params={
                "scope": scope.value,
                "q": serialized_query,
                "page": page,
            },
        )

    def get_service(
        self, queries: list[AbstractQuery] | None = None, page: int = 0
    ) -> AbstractResponse:
        """Shortcut for `get` with the scope `Scope.SERVICE`."""
        return self._parse_events(self.get(Scope.SERVICE, queries=queries, page=page))

    def get_leak(
        self, queries: list[AbstractQuery] | None = None, page: int = 0
    ) -> AbstractResponse:
        """Shortcut for `get` with the scope `Scope.LEAK`."""
        return self._parse_events(self.get(Scope.LEAK, queries=queries, page=page))

    def get_host(self, ipv4: str) -> AbstractResponse:
        """
        Returns the list of services and associated leaks for a given host. Only the ipv4 format is supported at the
        moment.
        """
        url = f"{self.base_url}/host/{ipv4}"
        return self._parse_host_result(self.__get(url, params=None))

    def get_plugins(self) -> AbstractResponse:
        """
        Returns the list of plugins the authenticated user with the given API key has access to.

        The output is a list of `APIResult` objects. The fields are `name` which is the plugin name, and `description`
        which contains a brief description of the plugin.
        Paid users have access to a broader list of plugins. The full list you can be found on
        https://leakix.net/plugins.
        For the paid plans, have a look at https://leakix.net/plans.
        """
        url = f"{self.base_url}/api/plugins"
        return self._parse_plugins(self.__get(url, params=None))

    def get_subdomains(self, domain: str) -> AbstractResponse:
        """
        Returns the list of subdomains for a given domain.
        The output is a list of `L9Subdomain` objects. The fields are `subdomain`, `distinct_ips` and `last_seen`.
        To get back a JSON/Python dictionary, use the method `to_dict` on the individual element of the response object.
        """
        url = f"{self.base_url}/api/subdomains/{domain}"
        return self._parse_subdomains(self.__get(url, params=None))

    def bulk_export(
        self, queries: list[AbstractQuery] | None = None
    ) -> AbstractResponse:
        url = f"{self.base_url}/bulk/search"
        params = {"q": serialize_queries(queries)}
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

    def bulk_export_last_event(
        self, queries: list[AbstractQuery] | None = None
    ) -> AbstractResponse:
        response = self.bulk_export(queries)
        if response.is_success():
            for aggreg in response.json():
                events = aggreg.events
                sorted_events = sorted(
                    events,
                    key=lambda event: event.time,
                    reverse=True,
                )
                aggreg.events = [sorted_events[0]]
        return response

    def bulk_service(
        self, queries: list[AbstractQuery] | None = None
    ) -> AbstractResponse:
        url = f"{self.base_url}/bulk/service"
        params = {"q": serialize_queries(queries)}
        r = requests.get(url, params=params, headers=self.headers, stream=True)
        if r.status_code == 200:
            response_json = []
            for line in r.iter_lines():
                json_event = json.loads(line)
                response_json.append(l9format.L9Event.from_dict(json_event))
            return SuccessResponse(response=r, response_json=response_json)
        elif r.status_code == 429:
            return RateLimitResponse(response=r)
        elif r.status_code == 204:
            return ErrorResponse(response=r, response_json=[], status_code=200)
        else:
            return ErrorResponse(response=r, response_json=r.json())
