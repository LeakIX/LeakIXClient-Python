import json
from pathlib import Path

import pytest
import requests_mock

from leakix import Client
from leakix.client import Scope
from leakix.field import CountryField, PluginField, PortField
from leakix.plugin import Plugin
from leakix.query import MustQuery, RawQuery

RESULTS_DIR = Path(__file__).parent / "results"
HOSTS_RESULTS_DIR = RESULTS_DIR / "host"
HOSTS_SUCCESS_RESULTS_DIR = HOSTS_RESULTS_DIR / "success"
HOSTS_404_RESULTS_DIR = HOSTS_RESULTS_DIR / "404"


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def client_with_api_key():
    return Client(api_key="test-api-key")


@pytest.fixture
def fake_ipv4():
    return "33.33.33.33"


class TestClientInit:
    def test_default_base_url(self):
        client = Client()
        assert client.base_url == "https://leakix.net"

    def test_custom_base_url(self):
        client = Client(base_url="https://custom.leakix.net")
        assert client.base_url == "https://custom.leakix.net"

    def test_api_key_in_headers(self):
        client = Client(api_key="my-api-key")
        assert client.headers["api-key"] == "my-api-key"

    def test_no_api_key_header_when_not_provided(self):
        client = Client()
        assert "api-key" not in client.headers

    def test_user_agent_header(self):
        client = Client()
        assert "leakix-client-python" in client.headers["User-agent"]

    def test_accept_header(self):
        client = Client()
        assert client.headers["Accept"] == "application/json"


class TestGetHost:
    def test_get_host_success(self, client):
        for f in HOSTS_SUCCESS_RESULTS_DIR.iterdir():
            with open(str(f)) as ff:
                res_json = json.load(ff)
            ipv4 = f.name[:-5]  # remove .json
            with requests_mock.Mocker() as m:
                url = f"{client.base_url}/host/{ipv4}"
                m.get(url, json=res_json, status_code=200)
                response = client.get_host(ipv4)
                assert response.is_success()
                assert len(response.json()["services"]) == 3
                assert response.json()["leaks"] is None

    def test_get_host_404(self, client):
        for f in HOSTS_404_RESULTS_DIR.iterdir():
            with open(str(f)) as ff:
                res_json = json.load(ff)
            ipv4 = f.name[:-5]  # remove .json
            with requests_mock.Mocker() as m:
                url = f"{client.base_url}/host/{ipv4}"
                m.get(url, json=res_json, status_code=404)
                response = client.get_host(ipv4)
                assert response.is_error()
                assert response.status_code() == 404
                assert response.json()["title"] == "Not Found"
                assert response.json()["description"] == "Host not found"

    def test_get_host_429(self, client, fake_ipv4):
        res_json = {"reason": "rate-limit", "status": "error"}
        with requests_mock.Mocker() as m:
            url = f"{client.base_url}/host/{fake_ipv4}"
            m.get(url, json=res_json, status_code=429)
            response = client.get_host(fake_ipv4)
            assert response.is_error()
            assert response.status_code() == 429
            assert response.json() == res_json


class TestGet:
    def test_get_with_empty_queries(self, client):
        res_json = []
        with requests_mock.Mocker() as m:
            m.get(f"{client.base_url}/search", json=res_json, status_code=200)
            response = client.get(Scope.SERVICE)
            assert response.is_success()
            assert m.last_request.qs["q"] == ["*"]
            assert m.last_request.qs["scope"] == ["service"]

    def test_get_with_must_query(self, client):
        res_json = []
        with requests_mock.Mocker() as m:
            m.get(f"{client.base_url}/search", json=res_json, status_code=200)
            queries = [MustQuery(CountryField("France"))]
            response = client.get(Scope.SERVICE, queries=queries)
            assert response.is_success()
            assert m.last_request.qs["q"] == ["+country:france"]

    def test_get_with_multiple_queries(self, client):
        res_json = []
        with requests_mock.Mocker() as m:
            m.get(f"{client.base_url}/search", json=res_json, status_code=200)
            queries = [
                MustQuery(CountryField("US")),
                MustQuery(PortField(443)),
            ]
            response = client.get(Scope.LEAK, queries=queries)
            assert response.is_success()
            assert m.last_request.qs["scope"] == ["leak"]

    def test_get_with_pagination(self, client):
        res_json = []
        with requests_mock.Mocker() as m:
            m.get(f"{client.base_url}/search", json=res_json, status_code=200)
            response = client.get(Scope.SERVICE, page=5)
            assert response.is_success()
            assert m.last_request.qs["page"] == ["5"]

    def test_get_with_negative_page_raises_error(self, client):
        with pytest.raises(ValueError, match="Page argument must be a positive"):
            client.get(Scope.SERVICE, page=-1)

    def test_get_204_returns_empty_list(self, client):
        with requests_mock.Mocker() as m:
            m.get(f"{client.base_url}/search", status_code=204)
            response = client.get(Scope.SERVICE)
            # 204 is converted to success with empty list
            assert response.json() == []


class TestGetService:
    def test_get_service_success_empty(self, client):
        # Test with empty response (no parsing needed)
        res_json = []
        with requests_mock.Mocker() as m:
            m.get(f"{client.base_url}/search", json=res_json, status_code=200)
            response = client.get_service()
            assert response.is_success()
            assert m.last_request.qs["scope"] == ["service"]

    def test_get_service_with_queries(self, client):
        res_json = []
        with requests_mock.Mocker() as m:
            m.get(f"{client.base_url}/search", json=res_json, status_code=200)
            queries = [MustQuery(PluginField(Plugin.GrafanaOpenPlugin))]
            response = client.get_service(queries=queries)
            assert response.is_success()
            # Verify query was serialized correctly
            assert "plugin:grafanaopenplugin" in m.last_request.qs["q"][0].lower()


class TestGetLeak:
    def test_get_leak_success(self, client):
        res_json = []
        with requests_mock.Mocker() as m:
            m.get(f"{client.base_url}/search", json=res_json, status_code=200)
            response = client.get_leak()
            assert response.is_success()
            assert m.last_request.qs["scope"] == ["leak"]


class TestGetPlugins:
    def test_get_plugins_success(self, client_with_api_key):
        res_json = [
            {"name": "GrafanaOpenPlugin", "description": "Grafana open instances"},
            {"name": "MongoOpenPlugin", "description": "MongoDB open instances"},
        ]
        with requests_mock.Mocker() as m:
            m.get(
                f"{client_with_api_key.base_url}/api/plugins",
                json=res_json,
                status_code=200,
            )
            response = client_with_api_key.get_plugins()
            assert response.is_success()
            assert len(response.json()) == 2

    def test_get_plugins_unauthorized(self, client):
        res_json = {"error": "unauthorized"}
        with requests_mock.Mocker() as m:
            m.get(f"{client.base_url}/api/plugins", json=res_json, status_code=401)
            response = client.get_plugins()
            assert response.is_error()


class TestGetSubdomains:
    def test_get_subdomains_success(self, client):
        res_json = [
            {
                "subdomain": "api.example.com",
                "distinct_ips": 2,
                "last_seen": "2024-01-01T00:00:00Z",
            },
            {
                "subdomain": "www.example.com",
                "distinct_ips": 1,
                "last_seen": "2024-01-01T00:00:00Z",
            },
        ]
        with requests_mock.Mocker() as m:
            m.get(
                f"{client.base_url}/api/subdomains/example.com",
                json=res_json,
                status_code=200,
            )
            response = client.get_subdomains("example.com")
            assert response.is_success()
            assert len(response.json()) == 2

    def test_get_subdomains_empty(self, client):
        with requests_mock.Mocker() as m:
            m.get(
                f"{client.base_url}/api/subdomains/unknown.com",
                json=[],
                status_code=200,
            )
            response = client.get_subdomains("unknown.com")
            assert response.is_success()
            assert response.json() == []


class TestBulkExport:
    def test_bulk_export_empty_success(self, client_with_api_key):
        # Test with empty response (no lines to parse)
        with requests_mock.Mocker() as m:
            m.get(
                f"{client_with_api_key.base_url}/bulk/search",
                text="",
                status_code=200,
            )
            response = client_with_api_key.bulk_export()
            assert response.is_success()
            assert response.json() == []

    def test_bulk_export_rate_limited(self, client_with_api_key):
        with requests_mock.Mocker() as m:
            m.get(
                f"{client_with_api_key.base_url}/bulk/search",
                json={"error": "rate-limit"},
                status_code=429,
            )
            response = client_with_api_key.bulk_export()
            assert response.is_error()
            assert response.status_code() == 429

    def test_bulk_export_204_empty(self, client_with_api_key):
        with requests_mock.Mocker() as m:
            m.get(
                f"{client_with_api_key.base_url}/bulk/search",
                status_code=204,
            )
            response = client_with_api_key.bulk_export()
            assert response.json() == []

    def test_bulk_export_query_serialization(self, client_with_api_key):
        with requests_mock.Mocker() as m:
            m.get(
                f"{client_with_api_key.base_url}/bulk/search",
                text="",
                status_code=200,
            )
            queries = [RawQuery("+plugin:Grafana +country:US")]
            client_with_api_key.bulk_export(queries=queries)
            assert "+plugin:grafana" in m.last_request.qs["q"][0].lower()


class TestBulkService:
    def test_bulk_service_empty_success(self, client_with_api_key):
        # Test with empty response (no lines to parse)
        with requests_mock.Mocker() as m:
            m.get(
                f"{client_with_api_key.base_url}/bulk/service",
                text="",
                status_code=200,
            )
            response = client_with_api_key.bulk_service()
            assert response.is_success()
            assert response.json() == []

    def test_bulk_service_204_empty(self, client_with_api_key):
        with requests_mock.Mocker() as m:
            m.get(
                f"{client_with_api_key.base_url}/bulk/service",
                status_code=204,
            )
            response = client_with_api_key.bulk_service()
            # 204 returns empty list
            assert response.json() == []

    def test_bulk_service_rate_limited(self, client_with_api_key):
        with requests_mock.Mocker() as m:
            m.get(
                f"{client_with_api_key.base_url}/bulk/service",
                json={"error": "rate-limit"},
                status_code=429,
            )
            response = client_with_api_key.bulk_service()
            assert response.is_error()
            assert response.status_code() == 429
