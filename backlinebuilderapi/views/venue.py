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
                
    def list(self, request ):
        """Handle GET requests to get all venues
        Returns:
            Response -- JSON serialized list of venues
        """
        venues = Venue.objects.all()
        
        location = request.query_params.get('location', None)
        if location is not None:
            venues = venues.filter(location_id=location)
            
        serializer = VenueSerializer(venues, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations
            
        Returns 
        Response -- JSON serialized venue gear instance
        """
            
        serializer = CreateVenueSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class VenueSerializer(serializers.ModelSerializer):
    """JSON serializer for venues"""
    
    class Meta:
        model = Venue 
        fields = ('id', 'location', 'name', 'address')
        depth = 4
        
class CreateVenueSerializer(serializers.ModelSerializer):
    """JSON serializer for venue gear
    """
    class Meta:
        model = Venue
        fields = ('id', 'location', 'name', 'address')