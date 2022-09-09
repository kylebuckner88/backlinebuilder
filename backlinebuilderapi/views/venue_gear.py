"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from backlinebuilderapi.models import VenueGear, Gear
from django.core.exceptions import ValidationError

class VenueGearView(ViewSet):
    """Backline builder venue gear view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single piece of gear
        
        Returns:
            Response -- JSON serialized gear
        """
        try: 
            venue_gear = VenueGear.objects.get(pk=pk)
            serializer = VenueGearSerializer(venue_gear)
            return Response(serializer.data)
        except Gear.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
                
    def list(self, request):
        """Handle GET requests to get all gear
        Returns:
            Response -- JSON serialized list of game types
        """
        venue_gear_list = VenueGear.objects.all()
        serializer = VenueGearSerializer(venue_gear_list, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations
        
        Returns 
            Response -- JSON serialized venue gear instance
        """
        serializer = CreateVenueGearSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        """ Handle PUT operations
        
        Returns
            Response -- JSON serialized game instance
        """
        venue_gear = VenueGear.objects.get(pk=pk)
        serializer = CreateVenueGearSerializer(venue_gear, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT) 
    
    def destroy(self, request, pk):
        venue_gear = VenueGear.objects.get(pk=pk)
        venue_gear.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT) 
    
class VenueGearSerializer(serializers.ModelSerializer):
    """JSON serializer for venue gear"""
    
    class Meta:
        model = VenueGear
        fields = ('venue_id', 'gear_id')
        
class CreateVenueGearSerializer(serializers.ModelSerializer):
    """JSON serializer for venue gear
    """
    class Meta:
        model = VenueGear
        fields = ['id', 'venue_id', 'gear_id']