from django.db import models
from django.contrib.auth.models import  AbstractBaseUser, PermissionsMixin, AbstractUser
from .managers import UserManeger


class User(AbstractBaseUser):
    phone_number = models.CharField(max_length=11, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    picture = models.FileField(blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email', 'name']

    objects = UserManeger()

    def __str__(self):
        return self.name

    def update(self, first_name, last_name, phone_number, email, password=None):
        change = False
        if first_name and last_name and phone_number and email:

            if self.first_name != first_name:
                self.first_name = first_name
                change = True

            if self.last_name != last_name:
                self.last_name = last_name
                change = True

            if self.phone_number != phone_number:
                self.phone_number = phone_number
                change = True

            if self.email != UserManeger.normalize_email(email):
                self.email = UserManeger.normalize_email(email)
                change = True

            if password:
                self.set_password(password)
                change = True

            if change:
                self.save()
        return self


    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    @property
    def is_authenticated (self):
        if self.phone_number:
            return True
        else:
            return False

    @property
    def is_anonymous(self):
        if self.phone_number:
            return False
        else:
            return True
    @property
    def name(self):
        return f'{self.first_name} {self.last_name}'
