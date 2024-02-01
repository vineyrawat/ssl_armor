from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('get_servers/', views.get_servers, name="get_servers"),
    path('add_server/', views.add_server, name="add_server"),
    path('force_sync/', views.force_sync, name="force_sync")
]