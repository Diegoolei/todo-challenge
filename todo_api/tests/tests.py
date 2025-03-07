from datetime import datetime, timedelta, timezone

# conftest.py
# conftest.py o tests.py
import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone as django_timezone
from rest_framework import status
from rest_framework.test import APIClient

from todo_api.models import Tag, Task


@pytest.fixture
def authenticated_user():
    User = get_user_model()
    return User.objects.create_user(
        username="testuser", email="test@example.com", password="testpass123"
    )


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_task(db):
    def _create_task(user=None):
        return Task.objects.create(title="Test Task", user=user)

    return _create_task


@pytest.fixture
def create_tasks(db):
    def _create_tasks(user, num_tasks):
        for i in range(num_tasks):
            Task.objects.create(title=f"Task {i}", user=user)

    return _create_tasks


@pytest.fixture
def create_tags(db):
    def _create_tags(user, num_tags):
        for i in range(num_tags):
            Tag.objects.create(name=f"Tag {i}", user=user)

    return _create_tags


@pytest.mark.django_db
def test_task_retrieve_success(authenticated_user, create_task):
    # Arrange
    task = create_task(user=authenticated_user)
    client = APIClient()
    client.force_authenticate(user=authenticated_user)

    # Act
    response = client.get(f"/api/tasks/{task.pk}/")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.data["title"] == task.title


@pytest.mark.django_db
def test_task_retrieve_unauthenticated(api_client, create_task, authenticated_user):
    # Arrange
    task = create_task(user=authenticated_user)
    # Act
    response = api_client.get(f"/api/tasks/{task.pk}/")
    # Assert
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_task_retrieve_not_found(authenticated_user, api_client):
    # Arrange
    api_client.force_authenticate(user=authenticated_user)
    invalid_pk = 999

    # Act
    response = api_client.get(f"/api/tasks/{invalid_pk}/")

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
@pytest.mark.parametrize(
    "title, description, priority, completed, finish_at, test_id",
    [
        (
            "Updated Groceries",
            "Buy cheese",
            2,
            True,
            django_timezone.now() + timedelta(days=2),
            "update-all-fields",
        ),
        ("Quick Errand", "Test Errand", 1, False, None, "update-some-fields"),
    ],
)
def test_task_update_success(
    authenticated_user,
    create_task,
    title,
    description,
    priority,
    completed,
    finish_at,
    test_id,
):
    # Arrange
    task = create_task(authenticated_user)
    client = APIClient()
    client.force_authenticate(user=authenticated_user)
    data = {
        "title": title,
        "description": description,
        "priority": priority,
        "completed": completed,
        "finish_at": finish_at,
    }

    # Act
    response = client.put(f"/api/tasks/{task.pk}/", data=data, format="json")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    task.refresh_from_db()
    assert task.title == title
    assert task.description == description
    assert task.priority == priority
    assert task.completed == completed
    if finish_at:
        assert task.finish_at == finish_at
    else:
        assert task.finish_at is None


@pytest.mark.django_db
def test_task_update_unauthenticated(api_client, create_task, authenticated_user):
    # Arrange
    task = create_task(user=authenticated_user)
    # Act
    response = api_client.put(
        f"/api/tasks/{task.pk}/",
        {"title": "Updated Title", "description": "Test Description"},
        format="json",
    )
    # Assert
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_task_update_not_found(authenticated_user, api_client):
    # Arrange
    api_client.force_authenticate(user=authenticated_user)
    invalid_pk = 999

    # Act
    response = api_client.put(f"/api/tasks/{invalid_pk}/", {"title": "Updated Title"})

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
@pytest.mark.parametrize(
    "title, error_message, test_id",
    [
        ("", "This field may not be blank.", "empty-title"),
        (
            "a" * 256,
            "Ensure this field has no more than 255 characters.",
            "too-long-title",
        ),
        (None, "This field may not be null.", "null-title"),
    ],
)
def test_task_update_invalid_data(
    authenticated_user, create_task, title, error_message, test_id
):
    # Arrange
    task = create_task(authenticated_user)
    client = APIClient()
    client.force_authenticate(user=authenticated_user)

    # Act
    response = client.put(f"/api/tasks/{task.pk}/", {"title": title}, format="json")

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert error_message in str(response.data)


@pytest.mark.django_db
def test_task_delete_success(authenticated_user, create_task):
    # Arrange
    task = create_task(authenticated_user)
    client = APIClient()
    client.force_authenticate(user=authenticated_user)

    # Act
    response = client.delete(f"/api/tasks/{task.pk}/")

    # Assert
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Task.objects.filter(pk=task.pk).exists()


@pytest.mark.django_db
def test_task_delete_unauthenticated(api_client, create_task, authenticated_user):
    # Arrange
    task = create_task(user=authenticated_user)

    # Act
    response = api_client.delete(f"/api/tasks/{task.pk}/")

    # Assert
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_task_delete_not_found(authenticated_user, api_client):
    # Arrange
    api_client.force_authenticate(user=authenticated_user)
    invalid_pk = 999

    # Act
    response = api_client.delete(f"/api/tasks/{invalid_pk}/")

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
@pytest.mark.parametrize(
    "name, test_id",
    [
        ("Groceries", "create-simple-tag"),
        ("Errands", "create-another-tag"),
        ("  Tag with spaces  ", "create-tag-with-leading-and-trailing-spaces"),
    ],
)
def test_tag_create_success(authenticated_user, name, test_id):
    # Arrange
    client = APIClient()
    client.force_authenticate(user=authenticated_user)
    data = {"name": name}

    # Act
    response = client.post("/api/tags/", data)

    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    tag = Tag.objects.get(name=name.strip())
    assert tag.user == authenticated_user
    assert tag.name == name.strip()


@pytest.mark.django_db
def test_tag_create_unauthenticated(api_client):
    # Act
    response = api_client.post("/api/tags/", {"name": "Test Tag"})

    # Assert
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
@pytest.mark.parametrize(
    "name, error_message, test_id",
    [
        ("", "This field may not be blank.", "empty-name"),
        (None, "This field may not be null.", "null-name"),
        (
            "a" * 256,
            "Ensure this field has no more than 30 characters.",
            "too-long-name",
        ),
    ],
)
def test_tag_create_invalid_data(authenticated_user, name, error_message, test_id):
    # Arrange
    client = APIClient()
    client.force_authenticate(user=authenticated_user)

    # Act
    response = client.post("/api/tags/", {"name": name}, format="json")

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert error_message in str(response.data)


@pytest.mark.django_db
def test_tag_list_authenticated(authenticated_user, create_tags):
    # Arrange
    create_tags(authenticated_user, 3)
    client = APIClient()
    client.force_authenticate(user=authenticated_user)

    # Act
    response = client.get("/api/tags/")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 3


@pytest.mark.django_db
def test_tag_list_unauthenticated(api_client):
    # Act
    response = api_client.get("/api/tags/")

    # Assert
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_mark_task_as_completed_success(authenticated_user, create_task):
    # Arrange
    task = create_task(authenticated_user)
    client = APIClient()
    client.force_authenticate(user=authenticated_user)

    # Act
    response = client.post(f"/api/tasks/{task.pk}/complete/", {})

    # Assert
    assert response.status_code == status.HTTP_200_OK
    task.refresh_from_db()
    assert task.completed
    assert response.data["completed"]


@pytest.mark.django_db
def test_mark_task_as_completed_unauthenticated(
    api_client, create_task, authenticated_user
):
    # Arrange
    task = create_task(user=authenticated_user)

    # Act
    response = api_client.post(f"/api/tasks/{task.pk}/complete/", {})

    # Assert
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_mark_task_as_completed_not_found(authenticated_user, api_client):
    # Arrange
    api_client.force_authenticate(user=authenticated_user)
    invalid_pk = 999

    # Act
    response = api_client.post(f"/api/tasks/{invalid_pk}/complete/", {})

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data == {"error": "Task not found"}


@pytest.mark.django_db
def test_get_queryset_authenticated(authenticated_user, create_tasks):
    # Arrange
    client = APIClient()
    client.force_authenticate(user=authenticated_user)
    create_tasks(authenticated_user, 3)

    # Act
    response = client.get("/api/tasks/")  # Call the view that uses get_queryset

    # Assert
    assert response.status_code == 200  # Check for successful response
    assert len(response.data) == 3  # Check that the correct number of tasks is returned


@pytest.mark.django_db
def test_get_queryset_unauthenticated(api_client, create_tasks, authenticated_user):
    # Arrange
    create_tasks(authenticated_user, 2)  # Create some tasks with no user assigned

    # Act
    response = api_client.get("/api/tasks/")

    # Assert
    assert (
        response.status_code == 401
    )  # Expect unauthorized access since no user is logged in


@pytest.mark.django_db
@pytest.mark.parametrize(
    "title, description, priority, completed, finish_at, test_id",
    [
        (
            "Groceries",
            "Buy milk",
            1,
            False,
            datetime.now(timezone.utc) + timedelta(days=1),
            "create-simple-task",
        ),
        (
            "Errands",
            "Pick up dry cleaning",
            2,
            True,
            None,
            "create-task-without-description-or-finish_at",
        ),
        (
            "   Valid with spaces  ",
            "Some description",
            3,
            False,
            None,
            "create-task-with-leading-and-trailing-spaces",
        ),
    ],
)
def test_perform_create_success(
    authenticated_user,
    title,
    description,
    priority,
    completed,
    finish_at,
    test_id,
):
    # Arrange
    client = APIClient()
    client.force_authenticate(user=authenticated_user)
    data = {
        "title": title,
        "description": description,
        "priority": priority,
        "completed": completed,
        "finish_at": finish_at,
    }

    # Act
    response = client.post("/api/tasks/", data, format="json")

    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    task = Task.objects.get(
        title=title.strip()
    )  # Strip spaces for consistent comparison
    assert task.user == authenticated_user
    assert task.description == description
    assert task.priority == priority
    assert task.completed == completed
    if finish_at:
        assert task.finish_at.replace(tzinfo=None) == finish_at.replace(
            tzinfo=None
        )  # Compare naive datetime objects
    else:
        assert task.finish_at is None


@pytest.mark.django_db
def test_perform_create_unauthenticated(api_client):
    # Act
    response = api_client.post("/api/tasks/", {"title": "Test Task"})

    # Assert
    assert (
        response.status_code == status.HTTP_401_UNAUTHORIZED
    )  # Expect unauthorized access since no user is logged in


@pytest.mark.django_db
@pytest.mark.parametrize(
    "title, error_message, test_id",
    [
        ("", "This field may not be blank.", "empty-title"),
        (
            "a" * 256,
            "Ensure this field has no more than 255 characters.",
            "too-long-title",
        ),
        (None, "This field may not be null.", "null-title"),
    ],
)
def test_perform_create_invalid_data(authenticated_user, title, error_message, test_id):
    # Arrange
    client = APIClient()
    client.force_authenticate(user=authenticated_user)

    # Act
    response = client.post("/api/tasks/", {"title": title}, format="json")

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert error_message in str(
        response.data
    )  # Check if the expected error message is present in the response
