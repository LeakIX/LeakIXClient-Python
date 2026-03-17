"""Shared logic between sync and async LeakIX clients."""

import dataclasses
from importlib.metadata import version
from typing import Any, cast

from l9format import l9format
from l9format.l9format import Model

from leakix.domain import L9Subdomain
from leakix.plugin import APIResult
from leakix.response import AbstractResponse

DEFAULT_URL = "https://leakix.net"


@dataclasses.dataclass
class HostResult(Model):
    Services: list[l9format.L9Event] | None = None
    Leaks: list[l9format.L9Event] | None = None


class BaseClient:
    """Shared initialization and response transformation logic."""

    MAX_RESULTS_PER_PAGE = 20

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = DEFAULT_URL,
    ) -> None:
        self.api_key = api_key
        self.base_url = base_url if base_url else DEFAULT_URL
        self.headers: dict[str, str] = {
            "Accept": "application/json",
            "User-agent": f"leakix-client-python/{version('leakix')}",
        }
        if api_key:
            self.headers["api-key"] = api_key

    @staticmethod
    def _parse_events(response: AbstractResponse) -> AbstractResponse:
        """Parse raw JSON dicts into L9Event objects on a success response."""
        if response.is_success():
            response.response_json = [
                l9format.L9Event.from_dict(res) for res in response.response_json
            ]
        return response

    @staticmethod
    def _parse_host_result(response: AbstractResponse) -> AbstractResponse:
        """Parse a host/domain response into {services, leaks} format."""
        if response.is_success():
            data: dict[str, Any] = response.json()
            formatted = cast(HostResult, HostResult.from_dict(data))
            response.response_json = {
                "services": formatted.Services,
                "leaks": formatted.Leaks,
            }
        return response

    @staticmethod
    def _parse_plugins(response: AbstractResponse) -> AbstractResponse:
        if response.is_success():
            response.response_json = [APIResult.from_dict(d) for d in response.json()]
        return response

    @staticmethod
    def _parse_subdomains(response: AbstractResponse) -> AbstractResponse:
        if response.is_success():
            response.response_json = [L9Subdomain.from_dict(d) for d in response.json()]
        return response
