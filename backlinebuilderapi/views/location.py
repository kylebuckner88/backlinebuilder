"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from backlinebuilderapi.models import Location
from django.core.exceptions import ValidationError

class LocationView(ViewSet):
    """Backline builder location view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single location
        
        Returns:
            Response -- JSON serialized location
        """
        try: 
            location = Location.objects.get(pk=pk)
            serializer = LocationSerializer(location)
            return Response(serializer.data)
        except Location.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
                
    def list(self, request):
        """Handle GET requests to get all locations
        Returns:
            Response -- JSON serialized list of locations
        """
        locations = Location.objects.all()
        
            
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations
        
        Returns 
        Response -- JSON serialized venue gear instance
        """
        serializer = CreateLocationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class LocationSerializer(serializers.ModelSerializer):
    """JSON serializer for locations"""
    
    class Meta:
        model = Location
        fields = ('id', 'city', 'state')
        depth = 3
        
class CreateLocationSerializer(serializers.ModelSerializer):
    """JSON serializer for venue gear
    """
    class Meta:
        model = Location
        fields = ('id', 'city', 'state')