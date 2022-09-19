"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from backlinebuilderapi.models import Gear
from django.core.exceptions import ValidationError

class GearView(ViewSet):
    """Backline builder gear view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single piece of gear
        
        Returns:
            Response -- JSON serialized gear
        """
        try: 
            gear = Gear.objects.get(pk=pk)
            serializer = GearSerializer(gear)
            return Response(serializer.data)
        except Gear.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
                
    def list(self, request):
        """Handle GET requests to get all gear
        Returns:
            Response -- JSON serialized list of game types
        """
        gearlist = Gear.objects.all()
        serializer = GearSerializer(gearlist, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations
        
        Returns 
        Response -- JSON serialized venue gear instance
        """
        serializer = CreateGearSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class GearSerializer(serializers.ModelSerializer):
    """JSON serializer for gear"""
    
    class Meta:
        model = Gear
        fields = ('id', 'type', 'name', 'maker')
        
class CreateGearSerializer(serializers.ModelSerializer):
    """JSON serializer for venue gear
    """
    class Meta:
        model = Gear
        fields = ('id', 'type', 'name', 'maker')
    
    
