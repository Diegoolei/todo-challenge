from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    DateTimeField,
    FileField,
    ForeignKey,
    ImageField,
    IntegerField,
    JSONField,
    ManyToManyField,
    Model,
    TextField,
    URLField,
)


class Tag(Model):
    user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    name = CharField(max_length=30)

    def __str__(self):
        return self.name


class Task(Model):
    user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)

    PRIORITY_CHOICES = ((1, "High"), (2, "Medium"), (3, "Low"))

    tags = ManyToManyField(Tag, blank=True)

    title = CharField(max_length=255)
    description = TextField(blank=True)
    priority = IntegerField(
        default=2,
        choices=PRIORITY_CHOICES,
        validators=[
            MinValueValidator(1, message="Value must be greater or equal to 1"),
            MaxValueValidator(3, message="Value must be less or equal to 3"),
        ],
    )
    completed = BooleanField(default=False)
    created_at = DateTimeField(auto_now_add=True, help_text="Task creation date")
    finish_at = DateTimeField(blank=True, null=True)
    parent_task = ForeignKey("self", on_delete=CASCADE, null=True, blank=True)

    attachment = FileField(upload_to="tasks/attachments/", null=True, blank=True)
    related_url = URLField(max_length=200, null=True, blank=True)
    image = ImageField(upload_to="tasks/images/", null=True, blank=True)
    extra_data = JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.user} - {self.priority}"
