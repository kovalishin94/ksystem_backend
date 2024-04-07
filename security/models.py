import uuid

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.cache import cache
from django.utils.timesince import timesince
from django.contrib.auth.models import User

from security import validators

class Permission(models.Model):
    name = models.CharField(max_length=4, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name


class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    email = models.EmailField(blank=True, unique=True, null=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    surname = models.CharField(max_length=255, blank=True)
    date_of_birth = models.DateField(blank=True, null=True, validators=[validators.validate_date_not_future])
    photo = models.ImageField(upload_to='user_photos/%Y/%m/%d', blank=True, null=True)
    permissions = models.ManyToManyField(Permission, related_name='profile', blank=True)
    last_seen = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['last_name']

    def __str__(self):
        return self.user.username
    
    def username(self):
        return self.user.username
    
    def human_last_seen(self):
        if self.last_seen:
            return timesince(self.last_seen)
    
    def is_online(self):
        if self.last_seen is not None and timezone.now() < self.last_seen + timezone.timedelta(seconds=300):
            return True
        return False

    def photo_url(self):
        if self.photo:
            return settings.SERVER_URL + self.photo.url
        else:
            return ''
        
    def human_created_at(self):
        return timesince(self.created_at)
    
    def human_updated_at(self):
        return timesince(self.updated_at)
    

