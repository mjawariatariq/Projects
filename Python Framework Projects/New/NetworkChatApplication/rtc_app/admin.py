# Django ka admin module import kar rahe hain
from django.contrib import admin
# Apni models ko import kar rahe hain
from .models import Room, Message

# Room model ko admin site pe register kar rahe hain
admin.site.register(Room)
# Message model ko admin site pe register kar rahe hain
admin.site.register(Message)
