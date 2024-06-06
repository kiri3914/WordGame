# wordgame/urls.py

from django.urls import path
from . import views


urlpatterns = [
    path('', views.game_home, name='game_home'),
    path('win/', views.game_win, name='game_win'),
    path('lose/', views.game_lose, name='game_lose'),
    path('history/', views.game_history, name='game_history'),
    path('history/<int:game_id>/', views.game_detail, name='game_detail'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('get_hint/', views.get_hint, name='get_hint')
]
