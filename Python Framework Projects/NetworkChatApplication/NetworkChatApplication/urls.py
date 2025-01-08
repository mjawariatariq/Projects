from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('rtc_app.urls')),  # Connects to the rtc_app routes
]
