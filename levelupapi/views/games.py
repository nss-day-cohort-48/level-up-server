"""View module for handling requests about games"""
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from levelupapi.models import Game, GameType, Gamer


class GameViewSet(ViewSet):

    def create(self, request):
        """[summary]

        Args:
            request ([type]): [description]

        Returns:
            [type]: [description]
        """
        gamer = Gamer.objects.get(user=request.auth.user)
        game_type = GameType.objects.get(pk=request.data['gameTypeId'])
        try:
            game = Game.objects.create(
                gamer=gamer,
                game_type=game_type,
                description=request.data['description'],
                name=request.data['name'],
                number_of_players=request.data['numberOfPlayers'],
                skill_level=request.data['skillLevel'],
                maker=request.data['maker'],
            )
            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single game

        Returns:
            Response -- JSON serialized game instance
        """
        try:
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8000/games/2
            #
            # The `2` at the end of the route becomes `pk`
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk):
        game = Game.objects.get(pk=pk)
        game_type = GameType.objects.get(pk=request.data['gameTypeId'])
        game.maker = request.data['maker']
        game.description = request.data['description']
        game.skill_level = request.data['skillLevel']
        game.name = request.data['name']
        game.number_of_players = request.data['numberOfPlayers']
        game.game_type = game_type

        game.save()

        serializer = GameSerializer(game, context={'request': request})

        return Response(serializer.data)

    def list(self, request):
        games = Game.objects.all()

        game_type = request.query_params.get('type', None)

        if game_type is not None:
            games = games.filter(game_type__id=game_type)

        serializer = GameSerializer(
            games, many=True, context={'request': request})

        return Response(serializer.data)

    def destroy(self, request, pk):
        try:
            game = Game.objects.get(pk=pk)
            game.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'
        # depth = 2
