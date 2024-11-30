from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth import get_user_model
from django.conf import settings

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user

# Create your models here.
class CustomUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        primary_key=True,
    )
    first_name = models.CharField(
        max_length=20,
        verbose_name='Имя',
        default='',
        blank=True
    )
    last_name = models.CharField(
        max_length=20,
        verbose_name='Фамилия',
        default='',
        blank=True
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name = 'Активный'
    )
    staff = models.BooleanField(
        default=False,
        verbose_name = 'Сотрудник'
    ) # a admin user; non super-user
    admin = models.BooleanField(
        default=False,
        verbose_name = 'Администратор'
    ) # a superuser
    password = models.CharField('Пароль', max_length=128)

    # notice the absence of a "Password field", that is built in.

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Email & Password are required by default.

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


def custom_user_model():
    return get_user_model()

def custom_user_foreign_key():
    return settings.AUTH_USER_MODEL

def custom_user(request):
    from django.shortcuts import get_object_or_404
    return get_object_or_404(CustomUser, email = request.user.email)