import pytest
from django.forms import model_to_dict
from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.response import Response
from rest_framework.reverse import reverse

from users.models import User
from users.serializers import UserSerializer, UpdateUserSerializer
from users.tests.factories import UserFactory
from users.tests.utils import sort_recursively, pick_random_obj, get_payload


@pytest.mark.django_db
def test_list(client, test_data):
    # Collect all response objects
    url = reverse('user-list')
    response_objs = []
    while url is not None:
        response: Response = client.get(url)
        assert response.status_code == status.HTTP_200_OK, response.data

        # If response is list - no pagination. Only one iteration is needed
        if isinstance(response.data, list):
            response_objs.extend(response.data)
            break
        else:  # Pagination is enabled, keep traversing pages
            url = response.data.get('next')
            response_objs.extend(response.data['results'])

    # Compare overall objects count
    queryset = User.objects.all()
    assert len(response_objs) == queryset.count()

    # Compare objects
    dummy_request = APIRequestFactory().request()
    serializer = UserSerializer(queryset, many=True, context={'request': dummy_request})
    sorted_response_objs, sorted_serializer_data = sort_recursively(response_objs), sort_recursively(serializer.data)
    assert sorted_response_objs == sorted_serializer_data  # Objects may differ in order, sort them before comparing


@pytest.mark.django_db
def test_create(client, serializer_context):
    """ Test ordinary creation and creation of existing object """
    url = reverse('user-list')
    data = {
        'username': 'user',
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'johndoe@gmail.com',
        'is_staff': True,
        'is_active': True,
        'is_superuser': False
    }

    # Test ordinary create case
    response: Response = client.post(url, data=data, format='json')
    assert response.status_code == status.HTTP_201_CREATED, response.data
    response.data.pop('date_joined')
    response.data.pop('url')
    assert response.data == data


@pytest.mark.django_db
def test_update(client, serializer_context, test_data):
    """ Test ordinary update and update with short_name that exists in another object """
    instance = pick_random_obj(User)
    url = reverse('user-detail', [instance.id])

    # Ordinary update (PUT)

    # Pass read-only attributes of initial company to safely compare dicts later
    new_user = UserFactory.build(date_joined=instance.date_joined, username=instance.username, id=instance.id)
    serializer = UpdateUserSerializer(instance=new_user, context=serializer_context)
    payload = get_payload(new_user, UpdateUserSerializer)
    response: Response = client.put(url, data=payload, format='json')
    assert response.status_code == status.HTTP_200_OK, response.data
    assert response.data == serializer.data

    # Test ordinary PATCH for every field available

    instance = pick_random_obj(User)
    url = reverse('user-detail', [instance.id])
    # Pass read-only attributes of initial company to safely compare dicts later
    new_user = UserFactory.build(date_joined=instance.date_joined, username=instance.username, id=instance.id)

    for field_name in payload.keys():  # Send PATCH request for each writeable field
        # Update existing instance with new field and serialize data to later compare it with response
        new_field_value = getattr(new_user, field_name)
        setattr(instance, field_name, new_field_value)
        serializer = UpdateUserSerializer(instance=instance, context=serializer_context)

        payload = get_payload(instance, UpdateUserSerializer, fields=[field_name])
        response: Response = client.patch(url, data=payload, format='json')
        assert response.status_code == status.HTTP_200_OK, response.data
        assert response.data == serializer.data


@pytest.mark.django_db
def test_detail(client, serializer_context, test_data):
    """ Test retrieving detail """
    obj = pick_random_obj(model_class=User)
    serializer = UserSerializer(instance=obj, context=serializer_context)

    # Ordinary detail request
    url = reverse('user-detail', [obj.id])
    response: Response = client.get(url)
    assert response.status_code == status.HTTP_200_OK, response.data
    assert response.data == serializer.data


@pytest.mark.django_db
def test_delete(client, test_data):
    obj = pick_random_obj(User)

    # Ordinary delete
    url = reverse('user-detail', [obj.id])
    response: Response = client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT, response.data


@pytest.mark.django_db
def test_detail_nonexistent(client, test_data):
    url = reverse(f'user-detail', [0])
    response: Response = client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_update_nonexistent(client, test_data):
    url = reverse('user-detail', [0])

    obj = pick_random_obj(User)

    # Test PUT
    response: Response = client.put(url, data=model_to_dict(obj), content_type='application/json')
    assert response.status_code == status.HTTP_404_NOT_FOUND

    # Test PATCH
    response: Response = client.patch(url, data=model_to_dict(obj), content_type='application/json')
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_delete_nonexistent(client, test_data):
    url = reverse('user-detail', [0])
    response: Response = client.delete(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
