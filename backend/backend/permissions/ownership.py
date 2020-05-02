from rest_framework import permissions

from rest_framework.generics import GenericAPIView


class OwnsObject(permissions.BasePermission):
    def has_permission(self, request, view):
        """Tries to check if an object belongs to the user
        ownership_field: The field in the object that corresponds to the user
        user_relation: The relation from user that owns the object

        Example:
        To check for
        article.author = user

        ownership_field = "author"
        user_relation = "user"
        """
        if not view.detail:
            return True
        queryset = view.filter_queryset(view.get_queryset())
        lookup_url_kwarg = view.lookup_url_kwarg or view.lookup_field
        filter_kwargs = {view.lookup_field: view.kwargs[lookup_url_kwarg]}
        ownership_field = view.ownership_field
        prefetch_field = "__".join(ownership_field.split("."))
        obj_qs = (
            queryset.filter(**filter_kwargs)
            .select_related(prefetch_field)
        )
        user_relation = getattr(view, "user_relation", "user")
        obj_field = obj_qs.first()
        for field in ownership_field.split("."):
            obj_field = getattr(obj_field, field)
        u_rel = request
        for field in user_relation.split("."):
            u_rel = getattr(u_rel, field)
        return obj_field == u_rel
