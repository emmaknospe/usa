from django.db import models

from profiles.models import Profile


class Post(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.TextField(max_length=40)
    text = models.TextField(max_length=3000)
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
# Create your models here.
