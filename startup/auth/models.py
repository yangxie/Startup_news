from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)

    ACTIVE = 'A'
    INACTIVE = 'I'
    STATUS_CHOICES = (
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=ACTIVE)

    updated_on = models.DateTimeField()
    bio = models.CharField(max_length=255, blank=True)
    profile_photo_url = models.CharField(max_length=2083, blank=True)

    state = models.CharField(max_length=2, blank=True, default='NA')
    city = models.CharField(max_length=35, blank=True)
    address = models.CharField(max_length=100, blank=True)
    zip = models.CharField(max_length=10, blank=True)
    country = models.CharField(max_length=2, blank=True, default='US')

    code = models.CharField(max_length=40, blank=True)
