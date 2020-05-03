from rest_framework.generics import ListAPIView, RetrieveAPIView
from ..mixins.prefetch import PrefetchQuerysetModelMixin


class PrefetchListAPIView(PrefetchQuerysetModelMixin, ListAPIView):
    """
    Concrete view for listing a prefetched queryset.
    """


class PrefetchRetrieveAPIView(PrefetchQuerysetModelMixin, RetrieveAPIView):
    """
    Concrete view for retrieving a prefetched queryset.
    """
