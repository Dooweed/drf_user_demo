from rest_framework import viewsets


class ActionBasedSerializerClassMixin(viewsets.GenericViewSet):
    """
        Adds possibility to dynamically choose serializer for your ModelViewSet depending on request action.
        To use this mixin inherit from it at your viewset (It must be before ModelViewSet parent).
        The default serializer is always used as fallback

        Example:
            # To use different serializer on list action just set attribute list_serializer_class at your viewset:

            class MyViewSet(ViewSet):
                serializer_class = MySerializer
                list_serializer_class = MyListSerializer

        With this code you will have MyListSerializer when action is 'list' and MySerializer for all other actions.
        The same patterns works for other action types: list, create, retrieve, update, partial_update and destroy.
        You just need to append _serializer_class to get desired attribute name.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_serializer_class(self):
        attr_name = f'{self.action}_serializer_class'
        if hasattr(self, attr_name):
            serializer_class = getattr(self, attr_name)
            self.serializer_class = serializer_class
        return super().get_serializer_class()
