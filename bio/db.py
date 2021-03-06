from django.db import models

class UserBio(models.Model):
    email = models.EmailField()
    secret = models.CharField(max_length=32)
    sequence = models.CharField(max_length=256)
    bio = models.TextField()
    name = models.TextField()
    avatar = models.TextField()
    twitter = models.TextField(null=True, blank=True)
    gplus = models.TextField(null=True, blank=True)
    date_added = models.DateTimeField()
    date_updated = models.DateTimeField()
    date_deleted = models.DateTimeField(null=True, blank=True)
