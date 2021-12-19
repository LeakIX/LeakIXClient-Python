import decouple
from leakix import Client
from leakix.query import MustQuery
from leakix.field import PluginField
from leakix.plugin import Plugin
from pprint import pprint

if __name__ == "__main__":
    while 1:
        api_key = decouple.config("API_KEY")
        client = Client(api_key=api_key)
        query_http_ntlm = MustQuery(field=PluginField(Plugin.HttpNTLM))
        response = client.get_host(ipv4="33.33.33.33")
        print("Status code: %d" % response.status_code())
        pprint(response.json())
