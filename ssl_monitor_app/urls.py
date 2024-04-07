from django.urls import path
from . import views
from knox import views as knox_views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='knox_login'),
    # path('create/', views.CreateUserView.as_view(), name="create"),
    path('logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
    path('profile/', views.ManageUserView.as_view(), name='profile'),
    path('get_servers/', views.get_servers, name="get_servers"),
    path('add_server/', views.add_server, name="add_server"),
    path('force_sync/', views.force_sync, name="force_sync"),
    path('update_email_config/', views.update_email_config, name="update_email_config"),
    path('get_email_config/', views.get_email_config, name="get_email_config"),
    path("test_email/", views.test_email, name="test_email")
]