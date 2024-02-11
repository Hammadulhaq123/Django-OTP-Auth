# Custom User Model:

from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from django.core.validators import RegexValidator, validate_email
from .managers import UserManager



phone_regex = RegexValidator(
    regex=r"^\d{10}", message="Phone number must contain 10 digits"
)

# Create your models here.
class UserModel(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=15, null=False, blank=False)
    last_name = models.CharField(max_length=20, null=False, blank=False)
    phone_number = models.CharField(unique=True, blank=False, null=False, max_length=10, validators=[phone_regex])
    email = models.EmailField(unique=True, max_length=50, null=True, blank=True, validators=[validate_email])
    otp = models.CharField(max_length=6)
    otp_expiry = models.DateTimeField(blank=True, null=True)
    max_otp_try = models.CharField(max_length=2, default=settings.MAX_OTP_TRY)
    otp_max_out = models.DateTimeField(blank=True, null=True)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    user_registered_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    objects = UserManager()

    def __str__(self):
        return self.email

