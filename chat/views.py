from django.shortcuts import render , redirect
from chat.models import Room, Message
from django.http import HttpResponse,JsonResponse
# Create your views here.

def home(request):
    return render(request,'home.html')

def room(request,room):
    print(room,"room")
    user_name = request.GET.get('username')
    room_details = Room.objects.get(name=room)

    return render(request, 'room.html',{
        "user_name":user_name,
        "room":room,
        "room_details":room_details
    })

def checkview(request):
    room_name = request.POST["room"]
    user_name = request.POST["name"]

    room_exist = Room.objects.filter(name=room_name).exists()
    print(room_exist,"room_exist")

    if room_exist:
        return redirect('/'+ room_name + '/?username='+user_name)
    else:
        new_room = Room.objects.create(name=room_name)
        new_room.save()
        return redirect('/'+ room_name + '/?username='+user_name)


def send(request):
    user_name = request.POST["username"]
    message = request.POST["message"]
    room_id = request.POST["room_id"]

    new_message = Message.objects.create(value=message,room=room_id,user=user_name)
    new_message.save()

    return HttpResponse('Meassage save successfully')

def getMessages(request,room):
    room_data = Room.objects.get(name=room)
    messages = Message.objects.filter(room=room_data.id)
    return JsonResponse({"messages":list(messages.values())})