"""Example usage of the async LeakIX client."""

import asyncio

import decouple

from leakix import AsyncClient, Scope

API_KEY = decouple.config("API_KEY")


async def example_search_services():
    """Search for services using a raw query string."""
    async with AsyncClient(api_key=API_KEY) as client:
        response = await client.search("+country:FR +port:22", scope=Scope.SERVICE)
        assert response.status_code() == 200
        for event in response.json():
            print(f"{event.ip}:{event.port} - {event.summary}")


async def example_search_leaks():
    """Search for leaks using a raw query string."""
    async with AsyncClient(api_key=API_KEY) as client:
        response = await client.search("+plugin:GitConfigHttpPlugin", scope=Scope.LEAK)
        assert response.status_code() == 200
        for event in response.json():
            print(f"{event.host} - {event.summary}")


async def main():
    await example_search_services()
    await example_search_leaks()


if __name__ == "__main__":
    asyncio.run(main())
