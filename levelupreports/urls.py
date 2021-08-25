from django.urls import path
from .views import usergame_list, events_by_user

urlpatterns = [
    path('reports/usergames', usergame_list),
    path('reports/userevents', events_by_user)
]
