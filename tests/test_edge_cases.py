"""Edge-case and validation tests for fields, queries, responses, and client."""

from datetime import datetime
from unittest.mock import Mock

import pytest
import requests_mock

from leakix import (
    AgeField,
    Client,
    CountryField,
    CustomField,
    ErrorResponse,
    IPField,
    MustQuery,
    Operator,
    PortField,
    RawQuery,
    Scope,
    SuccessResponse,
    TimeField,
)


class TestPortFieldEdgeCases:
    @pytest.mark.parametrize(
        "port",
        [-1, -100, 65536, 70000, 100000],
        ids=["neg-1", "neg-100", "65536", "70000", "100000"],
    )
    def test_invalid_ports(self, port):
        with pytest.raises((ValueError, AssertionError)):
            PortField(port)

    @pytest.mark.parametrize(
        "port",
        [0, 1, 80, 443, 8080, 65535],
        ids=["min", "one", "http", "https", "alt-http", "max"],
    )
    def test_valid_boundary_ports(self, port):
        field = PortField(port)
        assert field.serialize() == f"port:{port}"


class TestCustomFieldEdgeCases:
    def test_empty_string_value(self):
        field = CustomField("", "test_field")
        assert field.serialize() == "test_field:"

    def test_empty_string_field_name(self):
        field = CustomField("value", "")
        assert field.serialize() == ":value"

    def test_special_characters_in_value(self):
        field = CustomField("test value with spaces", "field")
        assert field.serialize() == "field:test value with spaces"


class TestCountryFieldEdgeCases:
    def test_empty_string(self):
        field = CountryField("")
        assert field.serialize() == "country:"

    def test_single_char(self):
        field = CountryField("X")
        assert field.serialize() == "country:X"


class TestIPFieldEdgeCases:
    def test_empty_string(self):
        field = IPField("")
        assert field.serialize() == "ip:"

    def test_ipv6_format(self):
        field = IPField("::1")
        assert field.serialize() == "ip:::1"


class TestAgeFieldEdgeCases:
    def test_zero_age(self):
        field = AgeField(0)
        assert field.serialize() == "age:0"

    def test_negative_age(self):
        field = AgeField(-1)
        assert field.serialize() == "age:-1"

    def test_large_age(self):
        field = AgeField(999999)
        assert field.serialize() == "age:999999"


class TestTimeFieldEdgeCases:
    def test_epoch_date(self):
        field = TimeField(datetime(1970, 1, 1))
        assert field.serialize() == 'time:"1970-01-01"'


class TestQueryEdgeCases:
    def test_raw_query_empty_string(self):
        query = RawQuery("")
        assert query.serialize() == ""

    def test_raw_query_special_chars(self):
        query = RawQuery('+host:*.example.com -port:"22"')
        assert query.serialize() == '+host:*.example.com -port:"22"'

    def test_must_query_with_all_operators(self):
        for op in Operator:
            field = CustomField("val", "f", op)
            query = MustQuery(field)
            result = query.serialize()
            assert result.startswith("+")


class TestClientEdgeCases:
    def test_none_api_key(self):
        client = Client(api_key=None)
        assert "api-key" not in client.headers

    def test_empty_string_api_key(self):
        client = Client(api_key="")
        assert "api-key" not in client.headers

    def test_none_base_url_uses_default(self):
        client = Client(base_url=None)
        assert client.base_url == "https://leakix.net"

    def test_empty_base_url_uses_default(self):
        client = Client(base_url="")
        assert client.base_url == "https://leakix.net"

    def test_get_with_none_queries(self):
        client = Client()
        with requests_mock.Mocker() as m:
            m.get(f"{client.base_url}/search", json=[], status_code=200)
            response = client.get(Scope.SERVICE, queries=None)
            assert response.is_success()
            assert m.last_request.qs["q"] == ["*"]

    def test_get_with_empty_query_list(self):
        client = Client()
        with requests_mock.Mocker() as m:
            m.get(f"{client.base_url}/search", json=[], status_code=200)
            response = client.get(Scope.SERVICE, queries=[])
            assert response.is_success()
            assert m.last_request.qs["q"] == ["*"]

    def test_get_page_zero(self):
        client = Client()
        with requests_mock.Mocker() as m:
            m.get(f"{client.base_url}/search", json=[], status_code=200)
            response = client.get(Scope.SERVICE, page=0)
            assert response.is_success()

    def test_get_negative_page(self):
        client = Client()
        with pytest.raises(ValueError):
            client.get(Scope.SERVICE, page=-1)


class TestResponseEdgeCases:
    def test_success_with_none_json(self):
        mock = Mock()
        mock.status_code = 200
        mock.json.return_value = None
        response = SuccessResponse(mock)
        assert response.json() is None

    def test_success_with_empty_list(self):
        mock = Mock()
        mock.status_code = 200
        response = SuccessResponse(mock, response_json=[])
        assert response.json() == []

    def test_error_with_custom_status_code(self):
        mock = Mock()
        mock.status_code = 503
        mock.json.return_value = {"error": "unavailable"}
        response = ErrorResponse(mock, status_code=503)
        assert response.status_code() == 503
