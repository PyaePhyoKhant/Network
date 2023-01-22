from django.contrib.auth.models import AbstractUser
from django.db import models
from crum import get_current_user
from django.urls import reverse


class User(AbstractUser):
    pass


class Post(models.Model):
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.created_by = get_current_user()
        super().save(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse("index")
