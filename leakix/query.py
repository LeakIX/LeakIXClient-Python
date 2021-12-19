from abc import ABCMeta, abstractmethod
from typing import Optional, List
from leakix.field import CustomField


class AbstractQuery(metaclass=ABCMeta):
    @abstractmethod
    def serialize(self) -> str:
        pass


class EmptyQuery(AbstractQuery):
    def serialize(self) -> str:
        return "*"


class Query(AbstractQuery):
    def __init__(self, field: CustomField):
        self.field = field


class MustQuery(Query):
    def serialize(self) -> str:
        return "+%s" % self.field.serialize()


class MustNotQuery(Query):
    def serialize(self) -> str:
        return "-%s" % self.field.serialize()


class ShouldQuery(Query):
    def serialize(self) -> str:
        return "%s" % self.field.serialize()
