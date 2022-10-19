import decouple
from leakix import Client
from leakix.query import MustQuery, MustNotQuery
from leakix.field import PluginField, CountryField
from leakix.plugin import Plugin


API_KEY = decouple.config("API_KEY")
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


if __name__ == "__main__":
    example_get_host_filter_plugin()
    example_get_service_filter_plugin()
    example_get_leaks_filter_multiple_plugins()
    example_get_leaks_multiple_filter_plugins_must_not()
