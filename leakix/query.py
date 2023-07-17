from abc import ABCMeta, abstractmethod
from typing import Optional, List
from leakix.field import CustomField


class AbstractQuery(metaclass=ABCMeta):
    """
    An abstract query. Should not be instantiated.
    """

    @abstractmethod
    def serialize(self) -> str:
        pass


class EmptyQuery(AbstractQuery):
    """
    Represents an empty query, which will be translated to a wildcard. Using an empty query means applying no filter on
    the results and the outputs of the query will be the latest results the engine found.
    """

    def serialize(self) -> str:
        return "*"


class Query(AbstractQuery):
    """
    A query for a custom field. Fields can be found on https://docs.leakix.net/docs/query/fields/
    A list of fields can be found in `field.py`.
    """

    def __init__(self, field: CustomField):
        self.field = field


class MustQuery(Query):
    """
    A MustQuery is a query that will impose a condition on the field, and will be translated to a `+query` in the API
    A list of fields can be found in `field.py`.
    """

    def serialize(self) -> str:
        return "+%s" % self.field.serialize()


class MustNotQuery(Query):
    """
    A MustNotQuery is a query that will exclude a condition on the field, and will be translated to a `-query` in the API
    A list of fields can be found in `field.py`.
    """

    def serialize(self) -> str:
        return "-%s" % self.field.serialize()


class ShouldQuery(Query):
    """
    A ShouldQuery is a query that will make the condition optional on the field, and will be translated to `query` in
    the API.
    A list of fields can be found in `field.py`.
    """

    def serialize(self) -> str:
        return "%s" % self.field.serialize()


class RawQuery(AbstractQuery):
    """
    A RawQuery is a query that can be used as on the website. For instance, to filter on the hosts `.be`, you can use
    RawQuery("+host:.be").
    """

    def __init__(self, raw_q: str):
        self.raw_q = raw_q

    def serialize(self) -> str:
        return self.raw_q
