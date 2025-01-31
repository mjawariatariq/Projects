from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Home page (list of rooms)
    path("", views.rooms, name="rooms"),
    # Login page
    path("login/", auth_views.LoginView.as_view(), name="login"),
    # Logout page
    path("logout/", views.logout_view, name="logout"),
    # Room page
    path("<str:slug>/", views.room, name="room"),
    # Room view for a specific room slug
    path("room/<str:room_slug>/", views.room_view, name="room_view"),
]
