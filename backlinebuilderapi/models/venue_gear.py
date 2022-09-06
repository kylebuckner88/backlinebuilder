from django.db import models
from backlinebuilderapi.models.gear import Gear
from backlinebuilderapi.models.venue import Venue


class VenueGear(models.Model):
    
    gear_id = models.ForeignKey(Gear, on_delete=models.CASCADE)
    venue_id = models.ForeignKey(Venue, on_delete=models.CASCADE)