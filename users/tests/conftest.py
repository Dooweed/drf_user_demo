import pytest
from django.http import HttpRequest
from rest_framework.request import Request
from rest_framework.test import APIClient, APIRequestFactory

from users.tests.factories import UserFactory


@pytest.fixture
def client() -> APIClient:
    return APIClient()


@pytest.fixture
def test_data() -> None:
    TEST_OBJECTS_AMOUNT = 20
    UserFactory.create_batch(TEST_OBJECTS_AMOUNT)


@pytest.fixture
def dummy_request() -> Request | HttpRequest:
    return APIRequestFactory().request()


@pytest.fixture
def serializer_context(dummy_request):
    return {'request': dummy_request}
