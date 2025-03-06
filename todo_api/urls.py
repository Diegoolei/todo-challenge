from django.urls import path

from .views import (
    TagListCreate,
    TagRetrieveUpdateDestroy,
    TaskListCreate,
    TaskRetrieveUpdateDestroy,
)

urlpatterns = [
    path("tasks/", TaskListCreate.as_view(), name="task-list-create"),
    path(
        "tasks/<int:pk>/",
        TaskRetrieveUpdateDestroy.as_view(),
        name="task-get-update-delete",
    ),
    path("tags/", TagListCreate.as_view(), name="tag-list-create"),
    path(
        "tags/<int:pk>/",
        TagRetrieveUpdateDestroy.as_view(),
        name="tag-get-update-delete",
    ),
]
