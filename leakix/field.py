from datetime import datetime
from enum import Enum

from leakix.plugin import Plugin


class Operator(Enum):
    StrictlyGreater = ">"
    StrictlySmaller = "<"
    Equal = ""


class CustomField:
    def __init__(
        self, v: str, field_name: str, operator: Operator | None = None
    ) -> None:
        if operator is None:
            operator = Operator.Equal
        self.operator = operator
        self.field_name = field_name
        self.v = v

    def serialize(self) -> str:
        if self.operator != Operator.Equal:
            res = f"{self.field_name}:{self.operator.value}{self.v}"
        else:
            res = f"{self.field_name}:{self.v}"
        return res


class TimeField(CustomField):
    def __init__(self, d: datetime, operator: Operator | None = None) -> None:
        v = '"{}"'.format(d.strftime("%Y-%m-%d"))
        super().__init__(v=v, operator=operator, field_name="time")


class UpdateDateField(CustomField):
    def __init__(self, d: datetime, operator: Operator | None = None) -> None:
        # v = '"%s"' % d.strftime("%Y-%m-%d %H:%M:%S")
        v = '"{}"'.format(d.strftime("%Y-%m-%d"))
        super().__init__(v=v, operator=operator, field_name="update_date")


class AgeField(CustomField):
    def __init__(self, age: int, operator: Operator | None = None) -> None:
        super().__init__(v=str(age), operator=operator, field_name="age")


class PluginField(CustomField):
    def __init__(self, p: Plugin) -> None:
        v = p.value
        super().__init__(v=v, operator=None, field_name="plugin")


class IPField(CustomField):
    def __init__(self, ip: str, operator: Operator | None = None) -> None:
        super().__init__(v=ip, operator=operator, field_name="ip")


class PortField(CustomField):
    def __init__(self, port: int, operator: Operator | None = None) -> None:
        assert 0 <= port < 65536
        super().__init__(v=str(port), operator=operator, field_name="port")


class CountryField(CustomField):
    def __init__(self, country: str) -> None:
        super().__init__(v=country, operator=None, field_name="country")
