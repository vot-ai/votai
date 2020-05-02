from typing import Iterator, TypeVar, Generic, Union
from django.db.models import QuerySet


T = TypeVar("T")  

class QueryType(Generic[T], QuerySet):
    def __iter__(self) -> Iterator[T]: ...
