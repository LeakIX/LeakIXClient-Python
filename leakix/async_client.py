"""Async LeakIX API client using httpx."""

import json
from collections.abc import AsyncIterator
from typing import Any, cast

import httpx
from l9format import l9format

from leakix.base import DEFAULT_URL, BaseClient
from leakix.client import Scope
from leakix.query import AbstractQuery, serialize_queries
from leakix.response import (
    AbstractResponse,
    ErrorResponse,
    RateLimitResponse,
    SuccessResponse,
)

DEFAULT_TIMEOUT = 30.0


class AsyncClient(BaseClient):
    """Async client for the LeakIX API.

    Mirrors the sync Client API but uses httpx for async operations.
    All methods return AbstractResponse for consistency with the sync client.
    """

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = DEFAULT_URL,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        super().__init__(api_key=api_key, base_url=base_url)
        self.timeout = timeout
        self._client: httpx.AsyncClient | None = None

    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create the HTTP client."""
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                headers=self.headers,
                timeout=self.timeout,
            )
        return self._client

    async def close(self) -> None:
        """Close the HTTP client."""
        if self._client is not None and not self._client.is_closed:
            await self._client.aclose()
            self._client = None

    async def __aenter__(self) -> "AsyncClient":
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()

    async def __get(
        self, path: str, params: dict[str, Any] | None = None
    ) -> AbstractResponse:
        """Make a GET request and return an AbstractResponse."""
        client = await self._get_client()
        r = await client.get(path, params=params)
        if r.status_code == 200:
            response_json = r.json() if r.content else []
            return SuccessResponse(response=r, response_json=response_json)
        if r.status_code == 429:
            return RateLimitResponse(response=r)
        if r.status_code == 204:
            return SuccessResponse(response=r, response_json=[])
        return ErrorResponse(response=r, response_json=r.json())

    async def get(
        self,
        scope: Scope,
        queries: list[AbstractQuery] | None = None,
        page: int = 0,
    ) -> AbstractResponse:
        """Search LeakIX for services or leaks."""
        if page < 0:
            raise ValueError("Page argument must be a positive integer")
        serialized_query = serialize_queries(queries)
        return await self.__get(
            "/search",
            params={"scope": scope.value, "q": serialized_query, "page": page},
        )

    async def get_service(
        self, queries: list[AbstractQuery] | None = None, page: int = 0
    ) -> AbstractResponse:
        """Shortcut for get with scope=Scope.SERVICE."""
        return self._parse_events(
            await self.get(Scope.SERVICE, queries=queries, page=page)
        )

    async def get_leak(
        self, queries: list[AbstractQuery] | None = None, page: int = 0
    ) -> AbstractResponse:
        """Shortcut for get with scope=Scope.LEAK."""
        return self._parse_events(
            await self.get(Scope.LEAK, queries=queries, page=page)
        )

    async def search(
        self, query: str, scope: Scope = Scope.LEAK, page: int = 0
    ) -> AbstractResponse:
        """
        Simple search using a raw query string (same syntax as the website).

        Example:
            >>> await client.search("+plugin:GitConfigHttpPlugin", scope=Scope.LEAK)
        """
        if page < 0:
            raise ValueError("Page argument must be a positive integer")
        r = await self.__get(
            "/search",
            params={"scope": scope.value, "q": query, "page": page},
        )
        return self._parse_events(r)

    async def get_host(self, ipv4: str) -> AbstractResponse:
        """Returns the list of services and associated leaks for a given host."""
        return self._parse_host_result(await self.__get(f"/host/{ipv4}"))

    async def get_domain(self, domain: str) -> AbstractResponse:
        """Returns the list of services and associated leaks for a given domain."""
        return self._parse_host_result(await self.__get(f"/domain/{domain}"))

    async def get_plugins(self) -> AbstractResponse:
        """Returns the list of plugins the authenticated user has access to."""
        return self._parse_plugins(await self.__get("/api/plugins"))

    async def get_plugin(self, name: str) -> AbstractResponse:
        """Returns the description of a plugin by its name."""
        return self._parse_plugin(await self.__get(f"/api/plugins/{name}"))

    async def get_subdomains(self, domain: str) -> AbstractResponse:
        """Returns the list of subdomains for a given domain."""
        return self._parse_subdomains(await self.__get(f"/api/subdomains/{domain}"))

    async def bulk_export(
        self, queries: list[AbstractQuery] | None = None
    ) -> AbstractResponse:
        """Bulk export leaks (Pro API feature)."""
        serialized_query = serialize_queries(queries)
        client = await self._get_client()
        async with client.stream(
            "GET", "/bulk/search", params={"q": serialized_query}
        ) as r:
            if r.status_code == 200:
                response_json = []
                async for line in r.aiter_lines():
                    if line:
                        json_event = json.loads(line)
                        response_json.append(
                            l9format.L9Aggregation.from_dict(json_event)
                        )
                return SuccessResponse(response=r, response_json=response_json)
            if r.status_code == 429:
                return RateLimitResponse(response=r)
            if r.status_code == 204:
                return SuccessResponse(response=r, response_json=[])
            await r.aread()
            return ErrorResponse(response=r, response_json=r.json())

    async def bulk_export_stream(
        self, queries: list[AbstractQuery] | None = None
    ) -> AsyncIterator[l9format.L9Aggregation]:
        """
        Streaming version of bulk_export. Yields L9Aggregation objects one by one.
        More memory efficient for large result sets.
        """
        serialized_query = serialize_queries(queries)
        client = await self._get_client()
        async with client.stream(
            "GET", "/bulk/search", params={"q": serialized_query}
        ) as r:
            if r.status_code != 200:
                return
            async for line in r.aiter_lines():
                if line:
                    json_event = json.loads(line)
                    yield cast(
                        l9format.L9Aggregation,
                        l9format.L9Aggregation.from_dict(json_event),
                    )
