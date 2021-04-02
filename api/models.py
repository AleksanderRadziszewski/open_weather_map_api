from django.db import models


class Temperature(models.Model):
    date = models.DateField()
    time = models.TimeField()
    temp = models.FloatField()
