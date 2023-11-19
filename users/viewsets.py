from adrf.viewsets import ViewSet as AsyncViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework import permissions, status
from rest_framework.response import Response

from users.filters import UserFilterSet, USER_SEARCH_FIELDS
from users.models import User
from users.serializers import UserSerializer, UpdateUserSerializer
from utils.rest_framework.viewsets.async_mixins import AsyncGetObjectMixin
from utils.rest_framework.viewsets.mixins import ActionBasedSerializerClassMixin


# Since adrf package doesn't support async ModelViewSet, we'll have to define all methods explicitly
class UserViewSet(ActionBasedSerializerClassMixin, AsyncGetObjectMixin, AsyncViewSet):
    """ List (`GET`), create (`POST`), retrieve (`GET`), update (`PUT`, `PATCH`) and destroy (`DELETE`) actions. """
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]  # Allowing any access since nothing is said about access restriction

    serializer_class = UserSerializer
    # We don't want users to be able to change some fields, so we use a different serializer for update
    update_serializer_class = UpdateUserSerializer
    partial_update_serializer_class = UpdateUserSerializer

    filter_backends = [OrderingFilter, DjangoFilterBackend, SearchFilter]
    filterset_class = UserFilterSet
    search_fields = USER_SEARCH_FIELDS
    ordering_fields = ('id', 'username', 'first_name', 'last_name', 'email', 'last_login', 'date_joined')
    ordering = ('-id',)

    async def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(await serializer.adata)

    async def retrieve(self, request, *args, **kwargs):
        instance = await self.aget_object()
        serializer = self.get_serializer(instance)
        return Response(await serializer.adata)

    async def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        await serializer.ais_valid(raise_exception=True)
        await serializer.asave()
        return Response(await serializer.adata, status=status.HTTP_201_CREATED)

    async def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = await self.aget_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        await serializer.ais_valid(raise_exception=True)
        await serializer.asave()

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(await serializer.adata)

    async def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return await self.update(request, *args, **kwargs)

    async def destroy(self, request, *args, **kwargs):
        instance = await self.aget_object()
        await instance.adelete()
        return Response(status=status.HTTP_204_NO_CONTENT)
