"""View module for handling requests about park areas"""
from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from levelupapi.models import Event, Gamer, Game

class Profile(ViewSet):

    def list(self, request):
        gamer = Gamer.objects.get(user=request.auth.user)
        events = Event.objects.filter(attendees=gamer)

        events = EventSerializer(events, many=True, context={'request': request})
        gamer = GamerSerializer(gamer, context={'request': request})

        profile = {
            'gamer': gamer.data,
            'events': events.data
        }

        return Response(profile)

class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for gamer's related Django user"""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')


class GamerSerializer(serializers.ModelSerializer):
    """JSON serializer for gamers"""
    user = UserSerializer(many=False)

    class Meta:
        model = Gamer
        fields = ('user', 'bio')


class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for games"""
    class Meta:
        model = Game
        fields = ('name',)


class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for events"""
    game = GameSerializer(many=False)

    class Meta:
        model = Event
        fields = ('id', 'game', 'description', 'date', 'time')
