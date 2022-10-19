from abc import ABCMeta, abstractmethod
import os
from typing import Optional, List
import requests
from pprint import pprint
from l9format import l9format
from enum import Enum
from serde import Model, fields
from leakix.response import SuccessResponse, ErrorResponse, RateLimitResponse
from leakix.query import *
from leakix.plugin import *
from leakix.field import *


class Scope(Enum):
    SERVICE = "service"
    LEAK = "leak"


class HostResult(Model):
    Services: fields.Optional(fields.List(fields.Nested(l9format.L9Event)))
    Leaks: fields.Optional(fields.List(fields.Nested(l9format.L9Event)))


class Client:
    BASE_URL = "https://leakix.net"
    VERSION = "0.1.0"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.headers = {
            "Accept": "application/json",
            "User-agent": "LeakIX-client-python/%s" % self.VERSION,
        }
        if api_key:
            self.headers["api-key"] = api_key

    def get(self, scope: Scope, queries: Optional[List[Query]] = None):
        if queries is None or len(queries) == 0:
            serialized_query = EmptyQuery().serialize()
        else:
            serialized_query = [q.serialize() for q in queries]
            serialized_query = " ".join(serialized_query)
            serialized_query = "%s" % serialized_query
        url = "%s/search" % self.BASE_URL
        r = requests.get(
            url,
            params={"scope": scope.value, "q": serialized_query},
            headers=self.headers,
        )
        if r.status_code == 200:
            response_json = r.json() or []
            return SuccessResponse(response=r, response_json=response_json)
        elif r.status_code == 429:
            return RateLimitResponse(response=r)
        else:
            return ErrorResponse(response=r, response_json=response.json())

    def get_service(self, queries: Optional[List[Query]] = None):
        r = self.get(Scope.SERVICE, queries=queries)
        if r.is_success():
            r.response_json = [
                l9format.L9Event.from_dict(res) for res in r.response_json
            ]
        return r

    def get_leak(self, queries: Optional[List[Query]] = None):
        r = self.get(Scope.LEAK, queries=queries)
        if r.is_success():
            r.response_json = [
                l9format.L9Event.from_dict(res) for res in r.response_json
            ]
        return r

    def get_host(self, ipv4: str):
        url = "%s/host/%s" % (self.BASE_URL, ipv4)
        r = requests.get(url, headers=self.headers)
        if r.status_code == 200:
            response_json = r.json()
            formatted_result = HostResult.from_dict(response_json)
            response_json = {
                "services": formatted_result.Services,
                "leaks": formatted_result.Leaks,
            }
            return SuccessResponse(response=r, response_json=response_json)
        elif r.status_code == 429:
            return RateLimitResponse(response=r)
        else:
            response_json = r.json()
            return ErrorResponse(response=r, response_json=response_json)
