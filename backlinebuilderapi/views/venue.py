"""View module for handling requests about venues"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from backlinebuilderapi.models import Venue
from django.core.exceptions import ValidationError

class VenueView(ViewSet):
    """Backline builder venue view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single venue
        
        Returns:
            Response -- JSON serialized venue
        """
        try: 
            venue = Venue.objects.get(pk=pk)
            serializer = VenueSerializer(venue)
            return Response(serializer.data)
        except Venue.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
                
    def list(self, request):
        """Handle GET requests to get all venues
        Returns:
            Response -- JSON serialized list of venues
        """
        venues = Venue.objects.all()
        serializer = VenueSerializer(venues, many=True)
        return Response(serializer.data)
    
class VenueSerializer(serializers.ModelSerializer):
    """JSON serializer for venues"""
    
    class Meta:
        model = Venue 
        fields = ('location_id', 'name', 'address')