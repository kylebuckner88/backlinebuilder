"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from backlinebuilderapi.models import VenueGear
from django.core.exceptions import ValidationError

class VenueGearView(ViewSet):
    """Backline builder venue gear view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single piece of gear
        
        Returns:
            Response -- JSON serialized gear
        """
        try: 
            venuegear = VenueGear.objects.get(pk=pk)
            serializer = VenueGearSerializer(venuegear)
            return Response(serializer.data)
        except VenueGear.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
                
    def list(self, request):
        """Handle GET requests to get all gear
        Returns:
            Response -- JSON serialized list of game types
        """
        venuegearlist = VenueGear.objects.all()
        
        # gear = request.query_params.get('gear', None)
        # if gear is not None:
        #     venuegearlist =venuegearlist.filter(gear_id=gear)
        
        serializer = VenueGearSerializer(venuegearlist, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations
        
        Returns 
            Response -- JSON serialized venue gear instance
        """
        serializer = CreateVenueGearSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        """ Handle PUT operations
        
        Returns
            Response -- JSON serialized game instance
        """
        venuegear = VenueGear.objects.get(pk=pk)
        serializer = CreateVenueGearSerializer(venuegear, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT) 
    
    def destroy(self, request, pk):
        gear = VenueGear.objects.get(pk=pk)
        gear.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT) 
    
class VenueGearSerializer(serializers.ModelSerializer):
    """JSON serializer for venue gear"""
    
    class Meta:
        model = VenueGear
        fields = ('id', 'gear', 'venue')
        depth = 2
        
class CreateVenueGearSerializer(serializers.ModelSerializer):
    """JSON serializer for venue gear
    """
    class Meta:
        model = VenueGear
        fields = ('id', 'venue', 'gear')
        depth = 3