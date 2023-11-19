from django_filters import rest_framework as filters

from users.models import User

USER_FILTERS = ('is_staff', 'is_active', 'is_superuser', 'date_joined')
USER_SEARCH_FIELDS = ('first_name', 'last_name')


class UserFilterSet(filters.FilterSet):
    date_joined = filters.DateFromToRangeFilter()

    class Meta:
        model = User
        fields = USER_FILTERS
