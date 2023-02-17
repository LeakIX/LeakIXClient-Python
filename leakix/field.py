from leakix.plugin import Plugin
from abc import ABCMeta, abstractmethod
from datetime import datetime
from typing import Optional
from enum import Enum


class Operator(Enum):
    StrictlyGreater = ">"
    StrictlySmaller = "<"
    Equal = ""


class CustomField:
    def __init__(self, v: str, field_name: str, operator: Optional[Operator] = None):
        if operator is None:
            operator = Operator.Equal
        self.operator = operator
        self.field_name = field_name
        self.v = v

    def serialize(self) -> str:
        if self.operator != Operator.Equal:
            res = "%s:%s%s" % (self.field_name, self.operator.value, self.v)
        else:
            res = "%s:%s" % (self.field_name, self.v)
        return res


class TimeField(CustomField):
    def __init__(self, d: datetime, operator: Optional[Operator] = None):
        v = d.strftime("%Y-%m-%d")
        super(TimeField, self).__init__(v=v, operator=operator, field_name="time")


class AgeField(CustomField):
    def __init__(self, age: int, operator: Optional[Operator] = None):
        super(AgeField, self).__init__(v=str(age), operator=operator, field_name="age")


class PluginField(CustomField):
    def __init__(self, p: Plugin):
        v = p.value
        super(PluginField, self).__init__(v=v, operator=None, field_name="plugin")


class IPField(CustomField):
    def __init__(self, ip: str, operator: Optional[Operator] = None):
        super(IPField, self).__init__(v=ip, operator=operator, field_name="ip")


class PortField(CustomField):
    def __init__(self, port: int, operator: Optional[Operator] = None):
        assert 0 <= port < 65536
        super(PortField, self).__init__(
            v=str(port), operator=operator, field_name="port"
        )


class CountryField(CustomField):
    def __init__(self, country: str):
        super(CountryField, self).__init__(
            v=country, operator=None, field_name="country"
        )
