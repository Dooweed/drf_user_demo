from django.http import Http404


class AsyncGetObjectMixin:
    """
        Adds an asynchronous version for .get_object() method.

        This class does not provide an exhaustive support for asynchronously getting object, since some code it uses
        may raise SynchronousOnlyOperation exception. Not ready for usage in other projects.
    """
    async def aget_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
                'Expected view %s to be called with a URL keyword argument '
                'named "%s". Fix your URL conf, or set the `.lookup_field` '
                'attribute on the view correctly.' %
                (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}

        obj = await queryset.filter(**filter_kwargs).afirst()
        if obj is None:
            raise Http404(
                "No %s matches the given query." % queryset.model._meta.object_name
            )

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj
