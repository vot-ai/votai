from collections import OrderedDict
from typing import Any, List
from rest_framework.routers import DefaultRouter, Route, DynamicRoute


class SingleInstanceRetrieveRouter(DefaultRouter):
    """Single Instance Retrieve Router

    All this does is allow viewsets whose "retrieve" methods should only
    return one instance to actually work like that and not require an "id" to be passed.

    To do so, set

    single_instance_viewset = True

    on the viewset
    """

    single_instance_routes = [
        # Detail route.
        Route(
            url=r"^{prefix}{trailing_slash}$",
            mapping={
                "post": "create",
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            },
            name="{basename}-detail",
            detail=False,
            initkwargs={"suffix": "Instance"},
        ),
        # Dynamically generated list routes. Generated using
        # @action(detail=False) decorator on methods of the viewset.
        DynamicRoute(
            url=r"^{prefix}/{url_path}{trailing_slash}$",
            name="{basename}-{url_name}",
            detail=False,
            initkwargs={},
        ),
        # Dynamically generated detail routes. Generated using
        # @action(detail=True) decorator on methods of the viewset.
        DynamicRoute(
            url=r"^{prefix}/{lookup}/{url_path}{trailing_slash}$",
            name="{basename}-{url_name}",
            detail=True,
            initkwargs={},
        ),
    ]

    def get_routes(self, viewset):
        baseroutes: List[Any] = self.routes
        if getattr(viewset, "single_instance_viewset", False):
            baseroutes = list(self.routes)
            self.routes = list(self.single_instance_routes)
        routes = super().get_routes(viewset)
        self.routes = baseroutes
        return routes

    def get_api_root_view(self, api_urls=None):
        """
        Return a basic root view.
        """
        api_root_dict = OrderedDict()
        list_name = self.routes[0].name
        single_instance_name = self.single_instance_routes[0].name
        for prefix, viewset, basename in self.registry:
            if getattr(viewset, "single_instance_viewset", False):
                api_root_dict[prefix] = single_instance_name.format(basename=basename)
            else:
                api_root_dict[prefix] = list_name.format(basename=basename)

        return self.APIRootView.as_view(api_root_dict=api_root_dict)
