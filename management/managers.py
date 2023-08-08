from django.contrib.auth.models import BaseUserManager


class UserManeger(BaseUserManager):
    def create_user(self, phone_number, email, first_name, last_name, password):
        if not phone_number:
            raise ValueError('user most have phone number')

        if not email:
            raise ValueError('user most have email')

        if not first_name:
            raise ValueError('user most have first name')

        if not last_name:
            raise ValueError('user most have last name')

        user = self.model(
            phone_number=phone_number,
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
                          )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, phone_number, email, first_name, last_name, password):
        user = self.create_user(phone_number, email, first_name, last_name, password)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self.db)
        return user


