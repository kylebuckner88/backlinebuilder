from django.db import models
from backlinebuilderapi.models.artist import Artist
from backlinebuilderapi.models.venue import Venue 

class Event(models.Model):
    
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    notes = models.CharField(max_length=1000)
    date = models.DateField()
    time = models.TimeField()