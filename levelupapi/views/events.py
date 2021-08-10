"""View module for handling requests about events"""
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from levelupapi.models import Game, Event, Gamer


class EventView(ViewSet):
    """Level up events"""

    def create(self, request):
        """Handle POST operations for events

        Returns:
            Response -- JSON serialized event instance
        """
        gamer = Gamer.objects.get(user=request.auth.user)

        event = Event()
        event.time = request.data["time"]
        event.date = request.data["date"]
        event.description = request.data["description"]
        event.host = gamer

        game = Game.objects.get(pk=request.data["gameId"])
        event.game = game

        try:
            event.save()
            serializer = EventSerializer(event, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single event

        Returns:
            Response -- JSON serialized game instance
        """
        try:
            event = Event.objects.get(pk=pk)
            serializer = EventSerializer(event, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for an event

        Returns:
            Response -- Empty body with 204 status code
        """
        organizer = Gamer.objects.get(user=request.auth.user)

        event = Event.objects.get(pk=pk)
        event.description = request.data["description"]
        event.date = request.data["date"]
        event.time = request.data["time"]
        event.host = organizer

        game = Game.objects.get(pk=request.data["gameId"])
        event.game = game
        event.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single game

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            event = Event.objects.get(pk=pk)
            event.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Event.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to events resource

        Returns:
            Response -- JSON serialized list of events
        """
        events = Event.objects.all()
        gamer = Gamer.objects.get(user=request.auth.user)
        # Support filtering events by game
        game = self.request.query_params.get('game_id', None)
        if game is not None:
            events = events.filter(game__id=game)

        for event in events:
            event.joined = gamer in event.attendees.all()

        serializer = EventSerializer(
            events, many=True, context={'request': request})
        return Response(serializer.data)

    @action(methods=['post', 'delete'], detail=True)
    def signup(self, request, pk):
        gamer = Gamer.objects.get(user=request.auth.user)
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
           return Response(
            {'message': 'Event does not exist.'},
            status=status.HTTP_404_NOT_FOUND
        )

        if request.method == "POST":
            try:
                event.attendees.add(gamer)
                return Response({}, status=status.HTTP_201_CREATED)
            except Exception as ex:
                return Response({'message': ex.args[0]})
        elif request.method == "DELETE":
            try:
                event.attendees.remove(gamer)
                return Response(None, status=status.HTTP_204_NO_CONTENT)
            except Exception as ex:
                return Response({'message': ex.args[0]})

class EventUserSerializer(serializers.ModelSerializer):
    """JSON serializer for event organizer's related Django user"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class EventGamerSerializer(serializers.ModelSerializer):
    """JSON serializer for event organizer"""
    user = EventUserSerializer(many=False)

    class Meta:
        model = Gamer
        fields = ['user']


class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for games"""
    class Meta:
        model = Game
        fields = ('id', 'name', 'maker', 'number_of_players', 'skill_level')


class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for events"""
    host = EventGamerSerializer(many=False)
    game = GameSerializer(many=False)

    class Meta:
        model = Event
        fields = ('id', 'game', 'host',
                  'description', 'date', 'time', 'joined')
