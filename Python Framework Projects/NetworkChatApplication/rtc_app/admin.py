# Django admin mein models ko register karna
from django.contrib import admin
from .models import Room, Message

admin.site.register(Room)
admin.site.register(Message)
