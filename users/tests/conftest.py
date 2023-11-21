import pytest
from django.http import HttpRequest
from rest_framework.request import Request
from rest_framework.test import APIClient, APIRequestFactory
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from users.tests.factories import UserFactory

test_user_credentials = {
    'username': 'admin',
    'password': '123'
}


@pytest.fixture
def client() -> APIClient:
    return APIClient()


@pytest.fixture
def admin_client() -> APIClient:
    user = User.objects.create_user(**test_user_credentials,
                                    pk=0,  # Set pk to zero so that admin user is not overridden by test data
                                    is_superuser=True, is_staff=True)
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    return client


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
