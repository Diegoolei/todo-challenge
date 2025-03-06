from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Tag, Task
from .serializers import TagSerializer, TaskSerializer


class TaskListCreate(ListCreateAPIView):
    """
    Supports filtering (priority, completed, created_at, finish_at),
    searching, and ordering.
    """

    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["priority", "completed", "created_at", "finish_at"]
    search_fields = ["title", "description"]
    ordering_fields = ["created_at", "finish_at", "priority"]

    def get_queryset(self):
        """
        Filters the queryset to return only tasks owned by the current user.

        Returns a queryset containing only the tasks associated with the
        authenticated user.
        """
        if not self.request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer: TaskSerializer):
        """Saves the new task with the authenticated user.

        Associates the current user with the new task before saving it to the
        database.
        """
        serializer.save(user=self.request.user)


class TaskRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"

    def get_queryset(self):
        """
        Filters the queryset to return only tasks owned by the current user.
        """
        if not self.request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return Task.objects.filter(user=self.request.user)


class TagListCreate(ListCreateAPIView):
    """
    Supports filtering (priority, completed, created_at, finish_at),
    searching, and ordering.
    """

    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["name", "user"]
    search_fields = ["name", "user"]

    def get_queryset(self):
        """
        Filters the queryset to return only tags owned by the current user.

        Returns a queryset containing only the tags associated with the
        authenticated user.
        """
        return Tag.objects.filter(user=self.request.user)

    def perform_create(self, serializer: TagSerializer):
        """Saves the new tag with the authenticated user.

        Associates the current user with the new tag before saving it to the
        database.
        """
        serializer.save(user=self.request.user)


class TagRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"

    def get_queryset(self):
        """
        Filters the queryset to return only tags owned by the current user.
        """
        return Tag.objects.filter(user=self.request.user)
