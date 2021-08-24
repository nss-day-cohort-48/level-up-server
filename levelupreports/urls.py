from django.urls import path
from .views import usergame_list

urlpatterns = [
    path('reports/usergames', usergame_list),
]
