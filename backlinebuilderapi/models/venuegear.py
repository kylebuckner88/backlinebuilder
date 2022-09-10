from django.db import models
from backlinebuilderapi.models.venue import Venue
from backlinebuilderapi.models.gear import Gear


class VenueGear(models.Model):
    
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    gear = models.ForeignKey(Gear, on_delete=models.CASCADE)