from timeit import default_timer

import pytest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from users.serializers import UserSerializer
from users.tests.factories import UserFactory
from users.tests.utils import pick_random_obj, get_payload


@pytest.mark.django_db
def test_user_can_edit_only_himself(client, test_data, serializer_context):
    """ Test that user without permissions on user model is able to see and change his own account and
    get 403 otherwise """
    list_url = reverse('user-list')

    obj = pick_random_obj(User)
    detail_url = reverse('user-detail', [obj.id])

    another_obj = UserFactory.build()
    payload = get_payload(another_obj, UserSerializer)

    # Accounting cannot do anything with other users
    user = UserFactory.create(username=str(default_timer()).replace('.', ''),  # Some random username so that it
                              # definitely does not overlap with existing Users
                              is_superuser=False)
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    user = User.objects.get(id=user.id)  # Object has changed
    self_detail_url = reverse('user-detail', [user.id])

    # Test create (403)
    response: Response = client.post(list_url, data=payload)
    assert response.status_code == status.HTTP_403_FORBIDDEN

    # Test update for another user (403)
    response: Response = client.put(detail_url, data=payload)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    response: Response = client.patch(detail_url, data=payload)
    assert response.status_code == status.HTTP_403_FORBIDDEN

    # Test delete for another user (403)
    response: Response = client.delete(detail_url)
    assert response.status_code == status.HTTP_403_FORBIDDEN

    # Test self update (200)
    payload.update({
        'username': str(default_timer()).replace('.', ''),
        # Faker generated username may collide with already existing ones
        'is_superuser': False,  # Must stay False
    })
    response: Response = client.put(self_detail_url, data=payload)
    assert response.status_code == status.HTTP_200_OK
    user = User.objects.get(id=user.id)  # Object has changed
    serializer = UserSerializer(user, context=serializer_context)
    assert response.data == serializer.data

    # Test self delete (204)
    response: Response = client.delete(self_detail_url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
