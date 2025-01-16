from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.rooms, name="rooms"),
    path("<str:slug>", views.room, name="room"),
    path("logout/", views.user_logout, name="logout"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
]
