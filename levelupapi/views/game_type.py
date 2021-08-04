"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from levelupapi.models import GameType


class GameTypeView(ViewSet):
    """The view for the GameType model

    methods:
        list: returns a list of all GameTypes
        retrieve: returns a single game type based on id
    """

    def retrieve(self, request, pk):
        """Retrieves a single GameType

        Args:
            request (Request): the request object
            pk (int): the id requested in the url

        Returns:
            Response: serialized gametype object
        """
        try:
            game_type = GameType.objects.get(pk=pk)
            serializer = GameTypeSerializer(
                game_type, context={'request': request})
            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Gets all game types in the database

        Args:
            request (Request): the request object

        Returns:
            Response: serialized list of all game types
        """
        game_types = GameType.objects.all()
        serializer = GameTypeSerializer(
            game_types, context={'request': request}, many=True)
        return Response(serializer.data)


class GameTypeSerializer(serializers.ModelSerializer):
    """GameType model serializer returns __all__ fields
    """
    class Meta:
        model = GameType
        fields = '__all__'
