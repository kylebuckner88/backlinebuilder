from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from backlinebuilderapi.models import Event, Artist

class EventView(ViewSet):
    "Backline Builder event view"""
    
    def retrieve(self, request, pk):
        """Handle GET requests for single event
        
        Returns:
            Response -- JSON serialized event
        """
        try:
            event = Event.objects.get(pk=pk)
            serializer = EventSerializer(event)
            return Response(serializer.data)
        except Event.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
            
    def list(self, request):
        """Handle GET requests to get all events
        Returns:
            Response -- JSON serialized list of events
        """
        events = Event.objects.all()
        venue_id = request.query_params.get('id', None)
        if venue_id is not None:
            event = events.filter(venue_id=venue_id)
        artist = Artist.objects.get(user=request.auth.user)
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations
        
        Returns
            Response -- JSON serialized game instance
        """
        artist = Artist.objects.get(user=request.auth.user)
        serializer = CreateEventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(organizer=artist)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        """ Handle PUT operations
        
        Returns
            Response -- JSON serialized game instance
        """
        event = Event.objects.get(pk=pk)
        serializer = CreateEventSerializer(event, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)  
    
    def destroy(self, request, pk):
        event = Event.objects.get(pk=pk)
        event.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT) 
            
class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for events"""
    
    class Meta:
        model = Event
        fields = ['artist', 'venue_id', 'notes', 'date', "time"]
        
class CreateEventSerializer(serializers.ModelSerializer):
    """JSON serializer for events
    """
    class Meta:
        model = Event
        fields = ['id', 'venue_id', 'notes', 'date', 'time']
        
        
        