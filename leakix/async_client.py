"""Async LeakIX API client using httpx."""

import asyncio
import json
from typing import AsyncIterator

import httpx
from l9format import l9format

from leakix.domain import L9Subdomain
from leakix.plugin import APIResult
from leakix.query import EmptyQuery, Query, RawQuery

__VERSION__ = "0.2.0"

DEFAULT_URL = "https://leakix.net"
DEFAULT_TIMEOUT = 30.0


class AsyncClient:
    """Async client for the LeakIX API."""

    MAX_RESULTS_PER_PAGE = 20

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = DEFAULT_URL,
        timeout: float = DEFAULT_TIMEOUT,
    ):
        self.api_key = api_key
        self.base_url = base_url if base_url else DEFAULT_URL
        self.timeout = timeout
        self.headers = {
            "Accept": "application/json",
            "User-agent": f"leakix-client-python/{__VERSION__}",
        }
        if api_key:
            self.headers["api-key"] = api_key
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

    async def __aexit__(self, *args) -> None:
        await self.close()

    async def _get(
        self,
        path: str,
        params: dict | None = None,
        max_retries: int = 3,
    ) -> tuple[int, dict | list | None]:
        """Make a GET request and return status code and JSON response.

        Automatically retries on rate limit (429) with exponential backoff.
        """
        client = await self._get_client()
        retries = 0
        delay = 1.0

        while True:
            response = await client.get(path, params=params)

            if response.status_code == 204:
                return response.status_code, []
            if response.status_code == 200:
                return response.status_code, response.json() if response.content else []
            if response.status_code == 429:
                if retries >= max_retries:
                    return response.status_code, None
                retries += 1
                await asyncio.sleep(delay)
                delay *= 2
                continue
            return response.status_code, response.json()

    async def get(
        self,
        scope: str,
        queries: list[Query] | None = None,
        page: int = 0,
    ) -> list[l9format.L9Event]:
        """
        Search LeakIX for services or leaks.

        Args:
            scope: Either "service" or "leak".
            queries: List of Query objects.
            page: Page number (0-indexed).

        Returns:
            List of L9Event results.
        """
        if page < 0:
            raise ValueError("Page argument must be a positive integer")
        if queries is None or len(queries) == 0:
            serialized_query = EmptyQuery().serialize()
        else:
            serialized_query = [q.serialize() for q in queries]
            serialized_query = " ".join(serialized_query)
            serialized_query = f"{serialized_query}"

        status, data = await self._get(
            "/search",
            params={"scope": scope, "q": serialized_query, "page": page},
        )
        if status == 200 and isinstance(data, list):
            return [l9format.L9Event.from_dict(item) for item in data]
        return []

    async def get_service(
        self,
        queries: list[Query] | None = None,
        page: int = 0,
    ) -> list[l9format.L9Event]:
        """Shortcut for get with scope='service'."""
        return await self.get("service", queries=queries, page=page)

    async def get_leak(
        self,
        queries: list[Query] | None = None,
        page: int = 0,
    ) -> list[l9format.L9Event]:
        """Shortcut for get with scope='leak'."""
        return await self.get("leak", queries=queries, page=page)

    async def search(
        self,
        query: str,
        scope: str = "leak",
        page: int = 0,
    ) -> list[l9format.L9Event]:
        """
        Simple search using a query string.

        Args:
            query: Search query string (same syntax as website).
            scope: Either "leak" or "service" (default: "leak").
            page: Page number for pagination (default: 0).

        Returns:
            List of L9Event results.
        """
        queries = [RawQuery(query)]
        if scope == "service":
            return await self.get_service(queries=queries, page=page)
        return await self.get_leak(queries=queries, page=page)

    async def get_host(self, ip: str) -> dict:
        """
        Get services and leaks for a specific IP address.

        Args:
            ip: IPv4 or IPv6 address.

        Returns:
            Dict with 'services' and 'leaks' lists.
        """
        status, data = await self._get(f"/host/{ip}")
        if status == 200 and isinstance(data, dict):
            services = data.get("Services") or []
            leaks = data.get("Leaks") or []
            return {
                "services": self._parse_events(services),
                "leaks": self._parse_events(leaks),
            }
        return {"services": [], "leaks": []}

    def _parse_events(self, items: list) -> list:
        """Parse events, falling back to raw dicts if l9format fails."""
        results = []
        for item in items:
            try:
                results.append(l9format.L9Event.from_dict(item))
            except Exception:
                results.append(item)
        return results

    async def get_domain(self, domain: str) -> dict:
        """
        Get services and leaks for a specific domain.

        Args:
            domain: Domain name.

        Returns:
            Dict with 'services' and 'leaks' lists.
        """
        status, data = await self._get(f"/domain/{domain}")
        if status == 200 and isinstance(data, dict):
            services = data.get("Services") or []
            leaks = data.get("Leaks") or []
            return {
                "services": self._parse_events(services),
                "leaks": self._parse_events(leaks),
            }
        return {"services": [], "leaks": []}

    async def get_subdomains(self, domain: str) -> list[L9Subdomain]:
        """
        Get subdomains for a domain.

        Args:
            domain: Domain name.

        Returns:
            List of L9Subdomain objects.
        """
        status, data = await self._get(f"/api/subdomains/{domain}")
        if status == 200 and isinstance(data, list):
            return [L9Subdomain.from_dict(d) for d in data]
        return []

    async def get_plugins(self) -> list[APIResult]:
        """
        Get list of available plugins.

        Returns:
            List of APIResult objects.
        """
        status, data = await self._get("/api/plugins")
        if status == 200 and isinstance(data, list):
            return [APIResult.from_dict(d) for d in data]
        return []

    async def bulk_export(
        self,
        queries: list[Query] | None = None,
    ) -> list[l9format.L9Aggregation]:
        """
        Bulk export leaks (Pro API feature).

        Args:
            queries: List of Query objects.

        Returns:
            List of L9Aggregation results.
        """
        if queries is None or len(queries) == 0:
            serialized_query = EmptyQuery().serialize()
        else:
            serialized_query = [q.serialize() for q in queries]
            serialized_query = " ".join(serialized_query)
            serialized_query = f"{serialized_query}"

        client = await self._get_client()
        results: list[l9format.L9Aggregation] = []

        async with client.stream(
            "GET", "/bulk/search", params={"q": serialized_query}
        ) as response:
            if response.status_code != 200:
                return results
            async for line in response.aiter_lines():
                if line:
                    data = json.loads(line)
                    results.append(l9format.L9Aggregation.from_dict(data))

        return results

    async def bulk_export_stream(
        self,
        queries: list[Query] | None = None,
    ) -> AsyncIterator[l9format.L9Aggregation]:
        """
        Streaming bulk export. Yields L9Aggregation objects one by one.

        Args:
            queries: List of Query objects.

        Yields:
            L9Aggregation objects as they arrive.
        """
        if queries is None or len(queries) == 0:
            serialized_query = EmptyQuery().serialize()
        else:
            serialized_query = [q.serialize() for q in queries]
            serialized_query = " ".join(serialized_query)
            serialized_query = f"{serialized_query}"

        client = await self._get_client()

        async with client.stream(
            "GET", "/bulk/search", params={"q": serialized_query}
        ) as response:
            if response.status_code != 200:
                return
            async for line in response.aiter_lines():
                if line:
                    data = json.loads(line)
                    yield l9format.L9Aggregation.from_dict(data)
