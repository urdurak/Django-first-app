from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, reverse
from .models import Chtmsg, Chtroom
from django.http import HttpResponseBadRequest, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .forms import MessageForm
from django.contrib import messages


# Create your views here.

@login_required(login_url=reverse_lazy('user-login'))
def inbox(request):
    messages = Chtmsg.objects.all()
    rooms = Chtroom.objects.all()
    return render(request, 'messages/chat-base-template.html', context={'msg': messages, 'rooms': rooms})


def personal_inbox(request, room_id):
    messg = Chtmsg.objects.all()
    roomlar = Chtroom.objects.all()
    roomlar2 = Chtroom.objects.filter(room_id=room_id)
    form = MessageForm()
    for i in roomlar2:
        if request.user != i.owner1:
            if request.user != i.owner2:
                return HttpResponseForbidden()
    context = {'messg': messg, 'rooms': roomlar, 'roomlar2': roomlar2, 'form': form}
    return render(request, 'messages/chatmessage.html', context=context)


def send_message(request, room_id):
    roomlar = Chtroom.objects.filter(room_id=room_id)
    form = MessageForm(data=request.POST or None)

    if form.is_valid():

        new_message = form.save(commit=False)
        new_message.sender = request.user
        for j in roomlar:
            if j.owner1 == request.user:
                new_message.receiver = j.owner2
                break
            else:
                new_message.receiver = j.owner1
                break
        new_message.save()
        messages.success(request, 'mesaj gitti')
        return HttpResponseRedirect(reverse('personal-inbox', kwargs={'room_id': room_id}))
