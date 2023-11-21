from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers
from adrf.serializers import Serializer as AsyncSerializer
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext as _

from users.models import User
from utils.rest_framework.serializers.async_validation import AsyncValidationMixin
from utils.rest_framework.serializers.fields import HyperlinkedIdentityField


class UserSerializer(AsyncSerializer, AsyncValidationMixin, serializers.HyperlinkedModelSerializer):
    url = HyperlinkedIdentityField(view_name='user-detail')
    username = serializers.CharField(max_length=150, validators=[UnicodeUsernameValidator])
    date_joined = serializers.DateTimeField(read_only=True)

    async def avalidate(self, attrs):
        if 'username' not in attrs:
            return attrs

        username = attrs['username']
        if await User.objects.filter(username=username).aexists():
            raise ValidationError({'username': _('A user with that username already exists.')})

        return attrs

    class Meta:
        model = User
        fields = ['url', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'date_joined',
                  'is_superuser']


class CreateUserSerializer(UserSerializer):
    @property
    def data(self):
        result = super().data

        if 'password' in result:
            result.pop('password')

        return result

    @property
    async def adata(self):
        result = await super().adata

        if 'password' in result:
            result.pop('password')

        return result

    async def acreate(self, validated_data):
        return await User.objects.acreate_user(**validated_data)

    class Meta:
        model = User
        fields = ['url', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'date_joined',
                  'is_superuser', 'password']


class UpdateUserSerializer(UserSerializer):
    username = serializers.CharField(read_only=True)

    async def aupdate(self, instance, validated_data):
        """ Original .update() also performs some additional logic on m2m and o2m relation,
         but since we don't have such on the user model, we don't need to do that work """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        await instance.asave()

        return instance

    class Meta(UserSerializer.Meta):
        pass
