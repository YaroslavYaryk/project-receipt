from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.db import models
from django.forms import DateTimeField

from .tasks import send_reset_password_email


class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError("Bruker må ha en e-postadresse")
        if not password:
            raise ValueError("Bruker må ha et passord")
        if not name:
            raise ValueError("empty name")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, name, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            name,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            name,
            password=password,
        )
        user.admin = True
        user.staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255, null=True)
    address = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=50, blank=True)
    postal_code = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=150, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    account_number = models.IntegerField(null=True, unique=True)

    is_active = models.BooleanField(default=True)  # can login
    admin = models.BooleanField(default=False)  # can login
    staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]
    objects = UserManager()

    def __str__(self):  # __unicode__ on Python 2
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
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    @property
    def is_staff(self):
        "Is the user a admin member?"
        return self.staff


from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
from django.template.loader import get_template
from django.core.mail import EmailMessage
from decouple import config
from django.conf import settings


@receiver(reset_password_token_created)
def password_reset_token_created(
    sender, instance, reset_password_token, *args, **kwargs
):

    return send_reset_password_email.delay(
        reset_password_token.key, reset_password_token.user.email
    )

    # email_plaintext_message = get_template("photo/product.html").render(
    #     {
    #         "token": reset_password_token.key,
    #         "image": f"{config('HOST')}:{config('PORT')}{settings.STATIC_URL + 'images/restaurant.jpg'}",
    #     }
    # )

    # mail = EmailMessage(
    #     subject="Password reset confirmation",
    #     body=email_plaintext_message,
    #     to=[reset_password_token.user.email],
    #     # reply_to=[EMAIL_ADMIN],
    # )
    # mail.content_subtype = "html"
    # return mail.send()
