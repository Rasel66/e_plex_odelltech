import re
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from accounts.choices import USER_TYPE_CHOICES

# Create your models here.
def phone_number_validator(value):
    pattern = r'^(\+8801|01)[3-9]\d{8}$'
    if not re.match(pattern, value):
        raise ValidationError('Enter a valid phone number')

class User(AbstractUser):
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    phone = models.CharField(max_length=20, validators=[phone_number_validator], blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='customer')

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"