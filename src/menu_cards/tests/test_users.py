import json

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status

DISHES_LIST = "dishes-list"
pytestmark = pytest.mark.django_db


def test_user_creation():
    User.objects.create_user("john", "lennon@thebeatles.com", "johnpassword")
    assert User.objects.count() == 1


def test_unauthorized_request(api_client):
    url = reverse(DISHES_LIST)
    response = api_client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_authorized_request_returns_200(token_client):
    url = reverse(DISHES_LIST)
    response = token_client.get(url)
    assert response.status_code == status.HTTP_200_OK


def test_superuser_authorized_request_returns_200(superadmin_client):
    url = reverse(DISHES_LIST)
    response = superadmin_client.get(url)
    assert response.status_code == status.HTTP_200_OK
