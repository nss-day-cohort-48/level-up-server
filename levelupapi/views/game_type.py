"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from levelupapi.models import GameType


class GameTypeView(ViewSet):
    def retrieve(self, request, pk):
        try:
            game_type = GameType.objects.get(pk=pk)
            serializer = GameTypeSerializer(
                game_type, context={'request': request})
            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        game_types = GameType.objects.all()
        serializer = GameTypeSerializer(
            game_types, context={'request': request}, many=True)
        return Response(serializer.data)

class GameTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameType
        fields = '__all__'
