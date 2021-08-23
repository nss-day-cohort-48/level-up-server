import json
from levelupapi.models.game import Game
from rest_framework import status
from rest_framework.test import APITestCase
from levelupapi.models import GameType

class GameTests(APITestCase):
    # fixtures = ['users', tokens, gametypes, games]
    def setUp(self):
        url = "/register"
        data = {
            "username": "steve",
            "password": "Admin8*",
            "email": "steve@stevebrownlee.com",
            "address": "100 Infinity Way",
            "phone_number": "555-1212",
            "first_name": "Steve",
            "last_name": "Brownlee",
            "bio": "Love those gamez!!"
        }

        response = self.client.post(url, data, format='json')
        self.token = response.data['token']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        gametype = GameType()
        gametype.label = "Board Game"
        gametype.save()

    def test_create_game(self):
        url = '/games'
        data = {
            "gameTypeId": 1,
            "skillLevel": 5,
            "name": "Clue",
            "maker": "Milton Bradley",
            "numberOfPlayers": 6,
            'description': "It's a fun game"
        }

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['maker'], data['maker'])
        self.assertEqual(response.data['skill_level'], data['skillLevel'])
        self.assertEqual(response.data['number_of_players'], data['numberOfPlayers'])
    
    def test_get_game(self):
        game = Game()
        game.game_type_id = 1
        game.skill_level = 5
        game.name = "Monopoly"
        game.maker = "Milton Bradley"
        game.description = "Not always fun"
        game.number_of_players = 4
        game.gamer_id = 1

        game.save()

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(f'/games/{game.id}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], game.name)
        self.assertEqual(response.data['maker'], game.maker)
        self.assertEqual(response.data['skill_level'], game.skill_level)
        self.assertEqual(response.data['number_of_players'], game.number_of_players)
        self.assertEqual(response.data['description'], game.description)

    def test_update_game(self):
        game = Game()
        game.game_type_id = 1
        game.skill_level = 5
        game.name = "Sorry"
        game.maker = "Milton Bradley"
        game.number_of_players = 4
        game.gamer_id = 1
        game.description = "It's fun"
        game.save()

        data = {
            "gameTypeId": 1,
            "skillLevel": 2,
            "name": "Sorry",
            "maker": "Hasbro",
            "numberOfPlayers": 4,
            "description": game.description
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.put(f'/games/{game.id}', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(f"/games/{game.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["skill_level"], data['skillLevel'])

    def test_delete_game(self):
        game = Game()
        game.game_type_id = 1
        game.skill_level = 5
        game.name = "Sorry"
        game.maker = "Milton Bradley"
        game.number_of_players = 4
        game.description = "It's a game"
        game.gamer_id = 1
        game.save()

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.delete(f'/games/{game.id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(f"/games/{game.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
