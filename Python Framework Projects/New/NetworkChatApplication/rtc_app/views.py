from pyexpat.errors import messages
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from rtc_app.models import Message, Room
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Room, Message

# Rooms view jo login required hoga
@login_required
def rooms(request):
    # Sab rooms ko fetch kar rahe hain
    rooms = Room.objects.all()
    # Rooms ko render kar rahe hain rooms.html template mein
    return render(request, "rooms.html", {"rooms": rooms})

# Room view jo login required hoga
@login_required
def room(request, slug):
    # Room ka name slug ke zariye fetch kar rahe hain
    room_name = Room.objects.get(slug=slug).name
    # Room ke messages ko filter kar rahe hain
    messages = Message.objects.filter(room=Room.objects.get(slug=slug))
    # Room aur messages ko render kar rahe hain room.html template mein
    return render(request, "room.html", {"room_name": room_name, "slug": slug, "messages": messages})

# Logout view jo user ko logout karayega aur login page pe redirect karega
def logout_view(request):
    """Logs out the user and redirects to the login page."""
    logout(request)  # User ko logout kar rahe hain
    messages.success(request, "You have been logged out successfully.")  # Flash message dikhana
    return redirect("login")  # Login page pe redirect kar rahe hain

# Room view jo room_slug ke zariye specific room ko show karega
def room_view(request, room_slug):
    room = Room.objects.get(slug=room_slug)  # Room ko slug ke zariye fetch kar rahe hain
    messages = room.message_set.all()  # Room ke saare messages fetch kar rahe hain
    # Room aur messages ko render kar rahe hain chat_room.html template mein
    return render(request, 'chat_room.html', {
        'room_name': room.name,
        'messages': messages,
    })
    
# Agar user login nahi hai toh login page pe redirect kar rahe hain
from django.shortcuts import render, redirect

def redirect_to_login(request):
    return redirect('login')  # Login page pe redirect kar rahe hain
