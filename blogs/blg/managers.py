from django.contrib.auth.models import PermissionsMixin, BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, name, email=None, mobile=None, password=None):

        if password is None:
            raise ValueError('Passowrd cannot be empty!')

        user = self.model(name=name, email=email, mobile=mobile, password=password)
        user.save()

        return user

    def create_superuser(self, firstname, lastname, email, mobile, password):

        if password is None:
            raise ValueError('Passowrd cannot be empty!')

        user = self.create_user(firstname, lastname, email, mobile, password)
        user.is_staff = True
        user.is_superuser = True
        user.save()

        return user