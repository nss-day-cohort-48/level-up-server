from django.contrib import admin
from levelupapi.models import Game, Gamer, Event, GameType

# Register your models here.
admin.site.register(Game)
admin.site.register(Gamer)
admin.site.register(Event)
admin.site.register(GameType)

