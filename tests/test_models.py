import pytest

from leakix.client import HostResult
from leakix.domain import L9Subdomain
from leakix.plugin import APIResult


class TestAPIResultSerialization:
    def test_to_dict(self):
        data = {"name": "GrafanaOpenPlugin", "description": "Grafana open instances"}
        obj = APIResult.from_dict(data)
        result = obj.to_dict()
        assert result["name"] == "GrafanaOpenPlugin"
        assert result["description"] == "Grafana open instances"

    def test_round_trip(self):
        data = {"name": "MongoOpenPlugin", "description": "MongoDB open instances"}
        first = APIResult.from_dict(data).to_dict()
        second = APIResult.from_dict(first).to_dict()
        assert first == second

    @pytest.mark.parametrize(
        "data",
        [
            {"name": "PluginA", "description": "Description A"},
            {"name": "PluginB", "description": ""},
            {"name": "", "description": "Empty name plugin"},
        ],
        ids=["normal", "empty-description", "empty-name"],
    )
    def test_round_trip_parametrized(self, data):
        first = APIResult.from_dict(data).to_dict()
        second = APIResult.from_dict(first).to_dict()
        assert first == second


class TestL9SubdomainSerialization:
    def test_to_dict(self):
        data = {
            "subdomain": "api.example.com",
            "distinct_ips": 3,
            "last_seen": "2024-01-15T10:30:00+00:00",
        }
        obj = L9Subdomain.from_dict(data)
        result = obj.to_dict()
        assert result["subdomain"] == "api.example.com"
        assert result["distinct_ips"] == 3
        assert "2024-01-15" in result["last_seen"]

    def test_round_trip(self):
        data = {
            "subdomain": "www.example.com",
            "distinct_ips": 1,
            "last_seen": "2024-06-20T12:00:00+00:00",
        }
        first = L9Subdomain.from_dict(data).to_dict()
        second = L9Subdomain.from_dict(first).to_dict()
        assert first == second

    @pytest.mark.parametrize(
        "data",
        [
            {
                "subdomain": "mail.example.com",
                "distinct_ips": 0,
                "last_seen": "2024-01-01T00:00:00+00:00",
            },
            {
                "subdomain": "a.b.c.example.com",
                "distinct_ips": 999,
                "last_seen": "2025-12-31T23:59:59+00:00",
            },
        ],
        ids=["zero-ips", "deep-subdomain"],
    )
    def test_round_trip_parametrized(self, data):
        first = L9Subdomain.from_dict(data).to_dict()
        second = L9Subdomain.from_dict(first).to_dict()
        assert first == second


class TestHostResultSerialization:
    def test_to_dict_empty(self):
        data = {"Services": None, "Leaks": None}
        obj = HostResult.from_dict(data)
        result = obj.to_dict()
        assert isinstance(result, dict)

    def test_round_trip_empty(self):
        data = {"Services": None, "Leaks": None}
        first = HostResult.from_dict(data).to_dict()
        second = HostResult.from_dict(first).to_dict()
        assert first == second
