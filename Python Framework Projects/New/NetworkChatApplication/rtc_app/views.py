from django.shortcuts import render, redirect
from django.contrib.auth import logout
from rtc_app.models import Message, Room
from django.contrib.auth.models import User

from django.shortcuts import render
from .models import Room,Message

def rooms(request):
    rooms=Room.objects.all()
    return render(request, "rooms.html",{"rooms":rooms})

from django.http import Http404, HttpResponseForbidden

def room(request, slug):
    try:
        room_name = Room.objects.get(slug=slug).name
    except Room.DoesNotExist:
        raise Http404("Room not found")
    messages = Message.objects.filter(room__slug=slug)
    return render(request, "room.html", {"room_name": room_name, "slug": slug, 'messages': messages})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')  # Redirect to login after logout
    return HttpResponseForbidden("Invalid method")


def room_view(request, room_slug):
    room = Room.objects.get(slug=room_slug)
    messages = room.message_set.all()  # Assuming the messages are related to rooms
    return render(request, 'chat_room.html', {
        'room_name': room.name,
        'messages': messages,
    })
