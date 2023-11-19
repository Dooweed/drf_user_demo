from django.contrib.auth.models import AbstractUser

from users.managers import AsyncUserManager


# We're just subclassing AbstractUser (along with everything that comes in PermissionsMixin) because it was not
# stated in the document whether presence or absence of permissions and groups is required
class User(AbstractUser):
    # Set these fields to None (they are defined in PermissionsMixin higher in mro), since they are not used
    groups = None
    user_permissions = None
    # Since we use JWT, we don't want to update this field (as it will lead to more DB queries and decrease
    # performance), therefore we don't need it at all
    last_login = None

    objects = AsyncUserManager()

    def __str__(self):
        """ Since first name and last name can be None, we'd prefer to use username if first name and
         last name are unavailable """
        return self.get_full_name_or_username()

    def get_full_name_or_username(self) -> str:
        """
        If first_name and/or last_name is not None, return first name and last name separated by space.
        Otherwise, return username
        """
        match (self.username, self.first_name, self.last_name):
            case (username, None | '', None | ''):
                return username
            case (_, first_name, None | ''):
                return first_name
            case (_, None | '', last_name):
                return last_name
            case (_, first_name, last_name):
                return f'{first_name} {last_name}'
            case _:
                raise ValueError(f'Username cannot be None')

    class Meta:
        verbose_name = AbstractUser.Meta.verbose_name
        verbose_name_plural = AbstractUser.Meta.verbose_name_plural

        # No indexes yet since no use case frequencies can be identified for now
        indexes = []

        ordering = ['id']
