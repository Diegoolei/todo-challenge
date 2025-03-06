from typing import Any

from drf_spectacular.utils import extend_schema_field
from rest_framework.serializers import (
    CurrentUserDefault,
    HiddenField,
    ModelSerializer,
    PrimaryKeyRelatedField,
    SerializerMethodField,
)

from .models import Tag, Task


class TagSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Tag
        fields = "__all__"
        read_only_fields = ["id"]


class TaskSerializer(ModelSerializer):
    tags = PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all(), required=False, write_only=True
    )

    tags_detail = SerializerMethodField(read_only=True)
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Task
        fields = "__all__"
        extra_fields = ["tags_detail"]
        read_only_fields = ["id", "created_at"]

    @extend_schema_field(TagSerializer(many=True))
    def get_tags_detail(self, obj: Task):
        """Uses SerializerMethodField to return tags as a list of dictionaries"""
        return TagSerializer(obj.tags.all(), many=True).data

    def create(self, validated_data: dict[str, Any]) -> Task:
        """Overwritten to handle tags"""
        tags_data = validated_data.pop("tags", [])
        task = Task.objects.create(**validated_data)
        task.tags.set(tags_data)
        return task

    def update(self, instance: Task, validated_data: dict[str, Any]) -> Task:
        """Overwritten to handle tags"""
        tags_data = validated_data.pop("tags", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if tags_data is not None:
            instance.tags.set(tags_data)
        instance.save()
        return instance
