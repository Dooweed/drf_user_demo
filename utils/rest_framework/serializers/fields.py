from rest_framework.relations import HyperlinkedIdentityField as DRFHyperlinkedIdentityField


class HyperlinkedIdentityField(DRFHyperlinkedIdentityField):
    """ A new version of HyperlinkedIdentityField that supports asynchronous version of .to_representation method """
    async def ato_representation(self, value):
        return self.to_representation(value)
