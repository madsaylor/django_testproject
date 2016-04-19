from django.db import models
from django.contrib.auth.models import User

class Link(models.Model):
    url = models.URLField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shortlink_path = models.CharField(max_length=1024)
