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


if __name__ == "__main__":
    example_get_host_filter_plugin()
    example_get_service_filter_plugin()
    example_get_service_filter_plugin_with_pagination()
    example_get_leaks_filter_multiple_plugins()
    example_get_leaks_multiple_filter_plugins_must_not()
    example_get_leak_plugins_with_time()
    example_get_leak_raw_query()
    example_get_plugins()
