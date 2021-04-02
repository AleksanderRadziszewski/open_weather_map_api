from django.db import models


class Temperature(models.Model):
    date = models.DateField()
    time = models.TimeField()
    temp = models.DecimalField(max_digits=4, decimal_places=2)
