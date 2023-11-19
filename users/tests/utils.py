import random
from typing import TypeVar, Type, Iterable

from django.db.models import QuerySet, Model
from rest_framework.fields import SkipField
from rest_framework.relations import PKOnlyObject
from rest_framework.serializers import Serializer
from rest_framework.test import APIRequestFactory


def sort_recursively(item: any, by_field: str = 'url'):
    """ This function sorts all lists in a response recursively and turns each OrderedDict to dict """

    def key_function(x):
        if isinstance(x, dict):
            return x[by_field]
        return x

    if isinstance(item, dict):
        item = dict(item)  # Convert OrderedDict to dict

        for key, val in item.items():
            item[key] = sort_recursively(val)
    elif isinstance(item, list | tuple):
        item.sort(key=key_function)

        for i, sub_item in enumerate(item):
            item[i] = sort_recursively(sub_item)

    return item


# For type hinting. IDE should know that the function return model instance
T = TypeVar('T')


def pick_random_obj(model_class: Type[T] = None, queryset: QuerySet[T] = None) -> T:
    """
        Pick a single random object from database
    :param model_class: Model class for desired object. You can specify queryset instead
    :param queryset: Queryset of desired objects. You can specify model_class instead
    :return: Django model object
    """
    assert (model_class is not None or queryset is not None) or (
                model_class and queryset), 'You must specify either model_class or queryset'

    queryset = queryset if queryset is not None else model_class.objects

    count = queryset.count()
    if count == 0:
        return None
    rand = random.randint(0, count - 1)
    return queryset.all().order_by('pk')[rand: rand + 1].first()


def get_payload(instance: Model, serializer_class: type(Serializer), fields: Iterable[str] = None,
                exclude_fields: Iterable[str] = None, exclude_null_values: bool = False) -> dict[str, any]:
    """
        Returns all writable fields of serializer class and their values from obj as dict.
        Useful for generating data for POST requests.
    :param instance: Model instance from which values will be gathered
    :param serializer_class: Serializer class to determine fields needed and serializer the data
    :param fields: Optionally pass fields to be included. Union of this parameter and writable serializer fields
        will be used as keys to returned dictionary
    :param exclude_fields: Optionally pass fields to be excluded. All fields from this parameter will be
        excluded if found in resulting dictionary
    :param exclude_null_values: If True, all values with value None will be excluded from resulting dictionary.
                                Can be useful if you want to use returned dictionary as payload for
                                form-encoded request. False by default.
    :return: Dictionary which can be used as payload.
    """
    data = {}

    serializer = serializer_class(instance, context={'request': APIRequestFactory().request()})

    for field_name, field in serializer.fields.items():
        if any((field.read_only,
                fields is not None and field_name not in fields,
                exclude_fields is not None and field_name in exclude_fields)):
            continue

        try:
            attribute = field.get_attribute(instance)
        except SkipField:
            continue

        # We skip `to_representation` for `None` values so that fields do
        # not have to explicitly deal with that case.
        #
        # For related fields with `use_pk_only_optimization` we need to
        # resolve the pk value.
        check_for_none = attribute.pk if isinstance(attribute, PKOnlyObject) else attribute
        if check_for_none is None:
            value = None
        else:
            try:
                value = field.to_representation(attribute)
            except ValueError as e:  # Reraise exception with field name information
                raise ValueError(f'Serializer field {field_name}') from e

        if exclude_null_values and value is None:
            continue

        data[field_name] = value

    return data
