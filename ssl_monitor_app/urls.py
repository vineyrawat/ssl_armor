from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('get_servers/', views.get_servers, name="get_servers"),
    path('add_server/', views.add_server, name="add_server"),
    path('force_sync/', views.force_sync, name="force_sync"),
    path('update_email_config/', views.update_email_config, name="update_email_config"),
    path('get_email_config/', views.get_email_config, name="get_email_config"),
    path("test_email/", views.test_email, name="test_email")
]