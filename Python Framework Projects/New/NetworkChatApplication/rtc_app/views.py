from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Room, Message

@login_required
def rooms(request):
    rooms = Room.objects.all()
    return render(request, "rooms.html", {"rooms": rooms})

@login_required
def room(request, slug):
    room_name = slug  # or fetch the room name from the database
    messages = Message.objects.filter(room__slug=slug).order_by('created_on')
    return render(request, 'room.html', {
        'room_name': room_name,
        'messages': messages,
        'slug': slug,
    })

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("login")

@login_required
def room_view(request, room_slug):
    room = get_object_or_404(Room, slug=room_slug)
    room_messages = room.message_set.all()
    return render(request, 'chat_room.html', {
        'room_name': room.name,
        'messages': room_messages,
    })
    
