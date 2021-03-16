from django.db import models


class Numbers(models.Model):
    text = models.CharField(max_length=100, blank=True)
    number = models.IntegerField(blank=True)
    found = models.BooleanField()
    type = models.CharField(max_length=100, blank=True)
