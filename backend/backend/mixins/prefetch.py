class PrefetchQuerysetModelMixin(object):
    """Prevents N+1 on large fetches

    Should be used on viewsets and views alongside PrefetchMixin
    """

    def get_queryset(self):
        assert self.queryset is not None
        queryset = self.queryset
        if hasattr(self.get_serializer_class(), "setup_eager_loading"):
            queryset = self.get_serializer().setup_eager_loading(queryset)
        return queryset


class PrefetchMixin(object):
    """Prevents N+1 problems on large fetches

    Should be a ModelSerializer mixin that contains one or both of the following Meta values:
    - select_related_fields
    - prefetch_related_fields

    These are, then, prefetch during serialization.
    """

    @classmethod
    def setup_eager_loading(cls, queryset):
        meta = cls.Meta
        if hasattr(meta, "select_related_fields"):
            queryset = queryset.select_related(*meta.select_related_fields)
        if hasattr(meta, "prefetch_related_fields"):
            queryset = queryset.prefetch_related(*meta.prefetch_related_fields)
        return queryset
