# LeakIX python client

[![](https://img.shields.io/pypi/v/leakix.svg)](https://pypi.org/project/leakix/)
[![](https://img.shields.io/pypi/pyversions/leakix.svg)](https://pypi.org/project/leakix/)

Official LeakIX python client

## Install

```
pip install leakix
```

To run tests, use `poetry run pytest`.

## Quick Start

```python
from leakix import Client

client = Client(api_key="your-api-key")

# Simple search - same syntax as the website
results = client.search("+plugin:GitConfigHttpPlugin", scope="leak")
for event in results.json():
    print(event.ip, event.host)

# Search services
results = client.search("+country:FR +port:22", scope="service")
```

## Async Client

For async applications, use `AsyncClient`:

```python
import asyncio
from leakix import AsyncClient

async def main():
    async with AsyncClient(api_key="your-api-key") as client:
        # Simple search
        results = await client.search("+plugin:GitConfigHttpPlugin", scope="leak")
        for event in results:
            print(event.ip, event.host)

        # Host lookup
        host = await client.get_host("8.8.8.8")
        print(host["services"])

        # Streaming bulk export
        async for aggregation in client.bulk_export_stream(queries):
            print(aggregation.events[0].ip)

asyncio.run(main())
```

## Documentation

Docstrings are used to document the library.
Types are also used to inform the user on what type of objects the functions are
expecting.

Each API response is encoded in either a `SuccessResponse` object or a
`ErrorResponse`.
The methods `is_success()` or `is_error()` exist on each API response.
You can get the actual response by using the method `json()` on the response object.

The output are events described in
[l9format](https://github.com/LeakIX/l9format-python).
When you have an object of type `l9Event` (or the longer
`l9format.l9format.L9Event`), you can refer to
[L9Event](https://github.com/LeakIX/l9format-python/blob/main/l9format/l9format.py#L158)
model class for the available fields.

For instance, to access the IP of an object `event` of type `L9Event`, you can
use `event.ip`.

Each object can be transformed back into a Python dictionary/JSON using the method `to_dict()`.
For instance, for the response of the subdomains endpoint, you can get back individual JSON by using:

```python
def example_get_subdomains():
    response = CLIENT.get_subdomains("leakix.net")
    for subdomain in response.json():
        print(subdomain.to_dict())
```

## Support

Feel free to open an issue if you have any question.
You can also contact us on `support@leakix.net`.

If you need commercial support, have a look at https://leakix.net/plans.

## Examples

```python
import decouple
from leakix import Client
from leakix.query import MustQuery, MustNotQuery, RawQuery
from leakix.field import PluginField, CountryField, TimeField, Operator
from leakix.plugin import Plugin
from datetime import datetime, timedelta


API_KEY = decouple.config("API_KEY")
BASE_URL = decouple.config("LEAKIX_HOST", default=None)
CLIENT = Client(api_key=API_KEY)


def example_get_host_filter_plugin():
    response = CLIENT.get_host(ipv4="33.33.33.33")
    assert response.status_code() == 200


def example_get_service_filter_plugin():
    """
    Filter by fields. In this example, we want to have the NTLM services.
    A list of plugins can be found in leakix.plugin
    """
    query_http_ntlm = MustQuery(field=PluginField(Plugin.HttpNTLM))
    response = CLIENT.get_service(queries=[query_http_ntlm])
    assert response.status_code() == 200
    # check we only get NTML related services
    assert all((i.tags == ["ntlm"] for i in response.json()))


def example_get_service_filter_plugin_with_pagination():
    """
    Filter by fields. In this example, we want to have the NTLM services.
    A list of plugins can be found in leakix.plugin.
    Ask for page 1 (starts at 0)
    """
    query_http_ntlm = MustQuery(field=PluginField(Plugin.HttpNTLM))
    response = CLIENT.get_service(queries=[query_http_ntlm], page=1)
    assert response.status_code() == 200
    # check we only get NTML related services
    assert all((i.tags == ["ntlm"] for i in response.json()))


def example_get_leaks_filter_multiple_plugins():
    query_http_ntlm = MustQuery(field=PluginField(Plugin.HttpNTLM))
    query_country = MustQuery(field=CountryField("France"))
    response = CLIENT.get_leak(queries=[query_http_ntlm, query_country])
    assert response.status_code() == 200
    assert all(
        (
            i.geoip.country_name == "France" and i.tags == ["ntlm"]
            for i in response.json()
        )
    )


def example_get_leaks_multiple_filter_plugins_must_not():
    query_http_ntlm = MustQuery(field=PluginField(Plugin.HttpNTLM))
    query_country = MustNotQuery(field=CountryField("France"))
    response = CLIENT.get_leak(queries=[query_http_ntlm, query_country])
    assert response.status_code() == 200
    assert all(
        (
            i.geoip.country_name != "France" and i.tags == ["ntlm"]
            for i in response.json()
        )
    )


def example_get_leak_raw_query():
    raw_query = '+plugin:HttpNTLM +country:"France"'
    query = RawQuery(raw_query)
    response = CLIENT.get_leak(queries=[query])
    assert response.status_code() == 200
    assert all(
        (
            i.geoip.country_name == "France" and i.tags == ["ntlm"]
            for i in response.json()
        )
    )


def example_get_leak_plugins_with_time():
    query_plugin = MustQuery(field=PluginField(Plugin.GitConfigHttpPlugin))
    today = datetime.now()
    one_month_ago = today - timedelta(days=30)
    query_today = MustQuery(field=TimeField(today, Operator.StrictlySmaller))
    query_yesterday = MustQuery(
        field=TimeField(one_month_ago, Operator.StrictlyGreater)
    )
    queries = [query_today, query_yesterday, query_plugin]
    response = CLIENT.get_leak(queries=queries)
    assert response.status_code() == 200


def example_get_plugins():
    response = CLIENT.get_plugins()
    for p in response.json():
        print(p.name)
        print(p.description)


def example_search_simple():
    """
    Simple search using query string syntax (same as the website).
    No need to build Query objects manually.
    """
    response = CLIENT.search("+plugin:GitConfigHttpPlugin", scope="leak")
    for event in response.json():
        print(event.ip)


def example_search_service():
    """
    Search for services with multiple filters.
    """
    response = CLIENT.search("+country:FR +port:22", scope="service")
    for event in response.json():
        print(event.ip, event.port)


def example_get_domain():
    """
    Get services and leaks for a domain.
    """
    response = CLIENT.get_domain("example.com")
    if response.is_success():
        print("Services:", response.json()["services"])
        print("Leaks:", response.json()["leaks"])


def example_bulk_stream():
    """
    Streaming bulk export - memory efficient for large datasets.
    Results are yielded one by one instead of loading all into memory.
    """
    query = MustQuery(field=PluginField(Plugin.GitConfigHttpPlugin))
    for aggregation in CLIENT.bulk_export_stream(queries=[query]):
        for event in aggregation.events:
            print(event.ip)


if __name__ == "__main__":
    example_get_host_filter_plugin()
    example_get_service_filter_plugin()
    example_get_service_filter_plugin_with_pagination()
    example_get_leaks_filter_multiple_plugins()
    example_get_leaks_multiple_filter_plugins_must_not()
    example_get_leak_plugins_with_time()
    example_get_leak_raw_query()
    example_get_plugins()
    example_search_simple()
    example_search_service()
    example_get_domain()
    example_bulk_stream()
```
