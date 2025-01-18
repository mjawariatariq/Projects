# Django ka models module aur User model ko import kar rahe hain
from django.db import models
from django.contrib.auth.models import User

# Room model define kar rahe hain
class Room(models.Model):
    # Room ka naam define kar rahe hain, max length 20 characters
    name = models.CharField(max_length=20)
    # Room ka slug define kar rahe hain, max length 100 characters
    slug = models.SlugField(max_length=100)

    # String representation define kar rahe hain
    def __str__(self):
        return "Room : "+ self.name + " | Id : " + self.slug

# Message model define kar rahe hain
class Message(models.Model):
    # Message ke liye user ko foreign key se connect kar rahe hain
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Message ka content text field mein store ho ga
    content = models.TextField()
    # Message ko kis room mein bheja gaya hai, room ko foreign key se connect kar rahe hain
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    # Message kab create hua, ye auto generate hoga jab message create ho ga
    created_on = models.DateTimeField(auto_now_add=True)

    # String representation define kar rahe hain
    def __str__(self):
        return "Message is :- "+ self.content
