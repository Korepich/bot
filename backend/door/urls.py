from django.urls import path

from .views import ActionCreateView, DoorCreateView, DoorRetrieveView, DoorListView, ActionListView

urlpatterns = [
    path(
        "api/v1/action/",
        ActionCreateView.as_view(
            {
                "post": "create",
            }
        ),
    ),
    path(
        "api/v1/action/list/",
        ActionListView.as_view(
            {
                "get": "list",
            }
        ),
    ),
    path(
        "api/v1/door/create/",
        DoorCreateView.as_view(
            {
                "post": "create",
            }
        ),
    ),
    path(
        "api/v1/door/<int:pk>/",
        DoorRetrieveView.as_view(
            {
                "get": "retrieve"
            }
        ),
    ),
    path(
        "api/v1/door/list/",
        DoorListView.as_view(
            {
                "get": "list"
            }
        ),
    ),
]
