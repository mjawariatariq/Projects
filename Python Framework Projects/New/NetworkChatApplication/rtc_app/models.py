from django.db import models
from django.contrib.auth.models import User

# Room model
class Room(models.Model):
    # Room name with a maximum length of 20 characters
    name = models.CharField(max_length=20)
    # Room slug with a maximum length of 100 characters
    slug = models.SlugField(max_length=100, unique=True)

    # String representation of the Room model
    def __str__(self):
        return f"Room: {self.name} | Slug: {self.slug}"

# Message model
class Message(models.Model):
    # ForeignKey to User model
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Message content stored as text
    content = models.TextField()
    # ForeignKey to Room model
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    # Timestamp for when the message was created
    created_on = models.DateTimeField(auto_now_add=True)

    # String representation of the Message model
    def __str__(self):
        return f"Message by {self.user.username}: {self.content}"
