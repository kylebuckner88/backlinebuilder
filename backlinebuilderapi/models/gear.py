from django.db import models
from backlinebuilderapi.models.venue import Venue 

class Gear(models.Model):
    
    type = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    maker = models.CharField(max_length=50)