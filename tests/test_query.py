from datetime import datetime

import pytest

from leakix import (
    AgeField,
    CountryField,
    CustomField,
    EmptyQuery,
    IPField,
    MustNotQuery,
    MustQuery,
    Operator,
    Plugin,
    PluginField,
    PortField,
    RawQuery,
    ShouldQuery,
    TimeField,
    UpdateDateField,
)


class TestEmptyQuery:
    def test_serialize_returns_wildcard(self) -> None:
        query = EmptyQuery()
        assert query.serialize() == "*"


class TestMustQuery:
    def test_serialize_with_country_field(self) -> None:
        field = CountryField("France")
        query = MustQuery(field)
        assert query.serialize() == "+country:France"

    def test_serialize_with_port_field(self) -> None:
        field = PortField(443)
        query = MustQuery(field)
        assert query.serialize() == "+port:443"

    def test_serialize_with_ip_field(self) -> None:
        field = IPField("192.168.1.1")
        query = MustQuery(field)
        assert query.serialize() == "+ip:192.168.1.1"


class TestMustNotQuery:
    def test_serialize_with_country_field(self) -> None:
        field = CountryField("China")
        query = MustNotQuery(field)
        assert query.serialize() == "-country:China"

    def test_serialize_with_port_field(self) -> None:
        field = PortField(22)
        query = MustNotQuery(field)
        assert query.serialize() == "-port:22"


class TestShouldQuery:
    def test_serialize_with_country_field(self) -> None:
        field = CountryField("Germany")
        query = ShouldQuery(field)
        assert query.serialize() == "country:Germany"


class TestRawQuery:
    def test_serialize_returns_raw_string(self) -> None:
        raw = '+plugin:HttpNTLM +country:"France"'
        query = RawQuery(raw)
        assert query.serialize() == raw

    def test_serialize_complex_query(self) -> None:
        raw = "+host:.be -port:22"
        query = RawQuery(raw)
        assert query.serialize() == raw


class TestCustomField:
    def test_serialize_without_operator(self) -> None:
        field = CustomField("test_value", "test_field")
        assert field.serialize() == "test_field:test_value"

    def test_serialize_with_equal_operator(self) -> None:
        field = CustomField("test_value", "test_field", Operator.Equal)
        assert field.serialize() == "test_field:test_value"

    def test_serialize_with_greater_operator(self) -> None:
        field = CustomField("100", "test_field", Operator.StrictlyGreater)
        assert field.serialize() == "test_field:>100"

    def test_serialize_with_smaller_operator(self) -> None:
        field = CustomField("100", "test_field", Operator.StrictlySmaller)
        assert field.serialize() == "test_field:<100"


class TestTimeField:
    def test_serialize_with_date(self) -> None:
        d = datetime(2024, 1, 15)
        field = TimeField(d)
        assert field.serialize() == 'time:"2024-01-15"'

    def test_serialize_with_greater_operator(self) -> None:
        d = datetime(2024, 1, 15)
        field = TimeField(d, Operator.StrictlyGreater)
        assert field.serialize() == 'time:>"2024-01-15"'

    def test_serialize_with_smaller_operator(self) -> None:
        d = datetime(2024, 1, 15)
        field = TimeField(d, Operator.StrictlySmaller)
        assert field.serialize() == 'time:<"2024-01-15"'


class TestUpdateDateField:
    def test_serialize_with_date(self) -> None:
        d = datetime(2024, 6, 20)
        field = UpdateDateField(d)
        assert field.serialize() == 'update_date:"2024-06-20"'


class TestAgeField:
    def test_serialize_with_age(self) -> None:
        field = AgeField(30)
        assert field.serialize() == "age:30"

    def test_serialize_with_greater_operator(self) -> None:
        field = AgeField(7, Operator.StrictlyGreater)
        assert field.serialize() == "age:>7"


class TestPluginField:
    def test_serialize_with_grafana_plugin(self) -> None:
        field = PluginField(Plugin.GrafanaOpenPlugin)
        assert field.serialize() == "plugin:GrafanaOpenPlugin"

    def test_serialize_with_mongodb_plugin(self) -> None:
        field = PluginField(Plugin.MongoOpenPlugin)
        assert field.serialize() == "plugin:MongoOpenPlugin"

    def test_serialize_with_http_ntlm_plugin(self) -> None:
        field = PluginField(Plugin.HttpNTLM)
        assert field.serialize() == "plugin:HttpNTLM"


class TestIPField:
    def test_serialize_with_ip(self) -> None:
        field = IPField("10.0.0.1")
        assert field.serialize() == "ip:10.0.0.1"


class TestPortField:
    def test_serialize_with_valid_port(self) -> None:
        field = PortField(8080)
        assert field.serialize() == "port:8080"

    def test_serialize_with_zero_port(self) -> None:
        field = PortField(0)
        assert field.serialize() == "port:0"

    def test_serialize_with_max_port(self) -> None:
        field = PortField(65535)
        assert field.serialize() == "port:65535"

    def test_invalid_port_negative(self) -> None:
        with pytest.raises(AssertionError):
            PortField(-1)

    def test_invalid_port_too_large(self) -> None:
        with pytest.raises(AssertionError):
            PortField(65536)

    def test_serialize_with_greater_operator(self) -> None:
        field = PortField(1024, Operator.StrictlyGreater)
        assert field.serialize() == "port:>1024"


class TestCountryField:
    def test_serialize_with_country(self) -> None:
        field = CountryField("US")
        assert field.serialize() == "country:US"

    def test_serialize_with_full_country_name(self) -> None:
        field = CountryField("France")
        assert field.serialize() == "country:France"
