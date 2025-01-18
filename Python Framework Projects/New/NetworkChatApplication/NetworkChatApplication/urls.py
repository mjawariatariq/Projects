from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin site ke liye URL path define kar rahe hain
    path('admin/', admin.site.urls),
    # Accounts app ke URLs ko include kar rahe hain (auth related URLs)
    path("accounts/", include("django.contrib.auth.urls")),
    # rtc_app ke URLs ko include kar rahe hain
    path('', include('rtc_app.urls')),
]
