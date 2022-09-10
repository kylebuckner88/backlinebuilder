from django.db import models
from backlinebuilderapi.models.location import Location


class Venue(models.Model):
    
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)