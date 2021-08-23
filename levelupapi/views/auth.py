from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from levelupapi.models import Gamer


@api_view(["POST"])
@permission_classes([AllowAny])
def login_user(request):
    """Checks if the user can log in and returns a valid token

    Args:
        request (Request): the request object

    Returns:
        Response: {
            valid: boolean, is it a real user?
            token: string, the token of the user
        }
    """
    username = request.data['username']
    password = request.data['password']

    authenticated_user = authenticate(username=username, password=password)
    data = {}
    if authenticated_user is not None:
        token = Token.objects.get(user=authenticated_user)
        data = {
            'valid': True,
            'token': token.key
        }
    else:
        data = {'valid': False}

    return Response(data)


@api_view(["POST"])
@permission_classes([AllowAny])
def register_user(request):
    """Registers a new user and creates their token

    Args:
        request (Request): the request object

    Returns:
        Response: {
            token: the newly created user's token
        }
    """
    new_user = User.objects.create_user(
        username=request.data['username'],
        email=request.data['email'],
        password=request.data['password'],
        first_name=request.data['first_name'],
        last_name=request.data['last_name']
    )

    gamer = Gamer.objects.create(
        bio=request.data['bio'],
        user=new_user
    )

    token = Token.objects.create(user=gamer.user)
    data = {
        'token': token.key
    }

    return Response(data, status=status.HTTP_201_CREATED)
