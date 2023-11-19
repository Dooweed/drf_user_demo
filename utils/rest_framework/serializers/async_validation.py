from rest_framework.exceptions import ValidationError
from rest_framework.fields import empty
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.serializers import as_serializer_error


class AsyncValidationMixin:
    """
        A small mixin that adds support for running asynchronous validation.
        It only supports a new async .avalidate() method.

        We need to run validation asynchronously for this project only for validating whether username exists or not.
        For making a mixin that handles whole validation asynchronously we'd need much more effort and time.
    """

    async def arun_validation(self, data=empty):
        """
        We override the default `run_validation`, because the validation
        performed by validators and the `.validate()` method should
        be coerced into an error dictionary with a 'non_fields_error' key.
        """
        (is_empty_value, data) = self.validate_empty_values(data)
        if is_empty_value:
            return data

        value = self.to_internal_value(data)
        try:
            self.run_validators(value)
            value = await self.avalidate(value)
            assert value is not None, '.validate() should return the validated data'
        except (ValidationError, DjangoValidationError) as exc:
            raise ValidationError(detail=as_serializer_error(exc))

        return value

    async def avalidate(self, attrs):
        return attrs

    async def ais_valid(self, *, raise_exception=False):
        assert hasattr(self, 'initial_data'), (
            'Cannot call `.is_valid()` as no `data=` keyword argument was '
            'passed when instantiating the serializer instance.'
        )

        if not hasattr(self, '_validated_data'):
            try:
                self._validated_data = await self.arun_validation(self.initial_data)
            except ValidationError as exc:
                self._validated_data = {}
                self._errors = exc.detail
            else:
                self._errors = {}

        if self._errors and raise_exception:
            raise ValidationError(self.errors)

        return not bool(self._errors)
