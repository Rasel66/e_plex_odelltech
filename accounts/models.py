import re
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

# Create your models here.
def phone_number_validator(value):
    pattern = r'^(\+8801|01)[3-9]\d{8}$'
    if not re.match(pattern, value):
        raise ValidationError('Enter a valid phone number')

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    phone = models.CharField(max_length=20, validators=[phone_number_validator], blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.username