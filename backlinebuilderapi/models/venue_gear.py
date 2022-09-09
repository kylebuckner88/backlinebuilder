from django.db import models
from backlinebuilderapi.models.venue import Venue
from backlinebuilderapi.models.gear import Gear


class VenueGear(models.Model):
    
    venue_id = models.ForeignKey(Venue, on_delete=models.CASCADE)
    gear_id = models.ForeignKey(Gear, on_delete=models.CASCADE)