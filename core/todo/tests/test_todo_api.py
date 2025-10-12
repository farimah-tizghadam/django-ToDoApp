import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from accounts.models import User, Profile
from todo.models import Task


@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.fixture
def common_user():
    user = User.objects.create_user(email="admin@admin.com", password="@/1234567")
    return user


@pytest.fixture
def another_user():
    user = User.objects.create_user(email="another@user.com", password="@/1234567")
    return user


@pytest.fixture
def common_profile(common_user):
    user = common_user
    profile = Profile.objects.create(
        user=user,
        first_name="test_first_name",
        last_name="test_last_name",
        description="test_description",
    )
    return profile


@pytest.fixture
def common_task(common_profile):
    user = common_profile
    task = Task.objects.create(user=user, title="test")
    return task


@pytest.mark.django_db
class TestTodoApi:

    def test_get_task_response_200_status(self, api_client):
        url = reverse("task:api-v1:task-list")
        response = api_client.get(url)
        assert response.status_code == 200

    def test_create_task_response_401_status(self, api_client):
        url = reverse("task:api-v1:task-list")
        data = {
            "title": "set up",
        }
        response = api_client.post(url, data)
        assert response.status_code == 401

    def test_create_task_response_201_status(self, api_client, common_user):
        url = reverse("task:api-v1:task-list")
        data = {
            "title": "set up project",
        }
        user = common_user
        api_client.force_authenticate(user=user)
        response = api_client.post(url, data)
        assert response.status_code == 201
        assert Task.objects.filter(title="set up project").exists()

    def test_create_task_detail_with_no_data_400_status_code(
        self, api_client, common_user
    ):
        url = reverse("task:api-v1:task-list")
        data = {}
        user = common_user
        api_client.force_authenticate(user=user)
        response = api_client.post(url, data)
        assert response.status_code == 400

    def test_create_task_detail_200_status_code(self, api_client, common_task):
        task = common_task
        url = reverse("task:api-v1:task-detail", kwargs={"pk": task.id})
        response = api_client.get(url)
        assert response.status_code == 200

    def test_update_task_forbidden_403_status_code(
        self, api_client, common_task, another_user
    ):

        task = common_task
        url = reverse("task:api-v1:task-detail", kwargs={"pk": task.id})
        data = {
            "title": "Unauthorized update",
            "complete": True,
        }

        api_client.force_authenticate(user=another_user)
        response = api_client.put(url, data)
        assert response.status_code == 403

    def test_update_task_detail_401_status_code(self, api_client, common_task):
        task = common_task
        url = reverse("task:api-v1:task-detail", kwargs={"pk": task.id})
        data = {
            "title": "set up project",
            "complete": True,
        }
        response = api_client.put(url, data)
        assert response.status_code == 401

    def test_update_task_detail_200_status_code(
        self, api_client, common_user, common_task
    ):
        task = common_task
        url = reverse("task:api-v1:task-detail", kwargs={"pk": task.id})
        data = {
            "title": "set up project",
            "complete": True,
        }
        user = common_user
        api_client.force_authenticate(user=user)
        response = api_client.put(url, data)
        assert response.status_code == 200

    @pytest.mark.parametrize(
        "field",
        [
            ("title"),
            ("complete"),
        ],
    )
    def test_partial_update_detail_401_status_code(
        self, api_client, common_task, field
    ):
        task = common_task
        url = reverse("task:api-v1:task-detail", kwargs={"pk": task.id})
        data = {"title": "set up project", "complete": True}
        valid_data = data[field]
        response = api_client.patch(url, {field: valid_data})
        assert response.status_code == 401

    @pytest.mark.parametrize(
        "field",
        [
            ("title"),
            ("complete"),
        ],
    )
    def test_partial_update_detail_200_status_code(
        self, api_client, common_task, common_user, field
    ):
        task = common_task
        url = reverse("task:api-v1:task-detail", kwargs={"pk": task.id})
        data = {"title": "set up project", "complete": True}
        user = common_user
        api_client.force_authenticate(user=user)
        valid_data = data[field]
        response = api_client.patch(url, {field: valid_data})
        assert response.status_code == 200

    def test_delete_task_detail_403_status_code(
        self, api_client, common_task, another_user
    ):
        task = common_task
        url = reverse("task:api-v1:task-detail", kwargs={"pk": task.id})

        api_client.force_authenticate(user=another_user)
        response = api_client.delete(url)
        assert response.status_code == 403

    def test_delete_task_detail_204_status_code(
        self, api_client, common_task, common_user
    ):
        task = common_task
        url = reverse("task:api-v1:task-detail", kwargs={"pk": task.id})
        user = common_user
        api_client.force_authenticate(user=user)
        response = api_client.delete(url)
        assert response.status_code == 204
