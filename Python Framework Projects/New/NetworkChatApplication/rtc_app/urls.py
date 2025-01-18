from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

# URL patterns define kar rahe hain
urlpatterns = [
    # Rooms view ke liye URL path
    path("", views.rooms, name="rooms"),
    # Login view ke liye URL path
    path("login/", auth_views.LoginView.as_view(), name="login"),
    # Logout view ke liye URL path, logout hone ke baad login page pe redirect hoga
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
    # Room ke liye URL path, slug ke zariye specific room ko access kar rahe hain
    path("<str:slug>", views.room, name="room"),
]
