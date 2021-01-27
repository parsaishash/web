from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'base'

urlpatterns = [
    path('tet/', views.tet, name='tet'),
    path('', views.authen, name='authen'),
    path('wel/', views.wel, name='wel'),
    path('upload/', views.upload, name='upload'),
    path('player/<str:play_path>', views.player, name='player'),
    path('download/<str:path>', views.down, name='down'),
    path('<str:wich_type>/home', views.home, name='home'),
    path('goـtoـdirectory/<str:path>/<str:wich_type>', views.go_to_directory, name='go_to_directory'), 
]
