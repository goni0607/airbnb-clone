from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView
from . import models
from rooms import models as room_models


def toggle_view(request, room_pk):
    room = room_models.Room.objects.get_or_none(pk=room_pk)
    action = request.GET.get("action", None)
    if room is not None and action is not None:
        my_list, _ = models.List.objects.get_or_create(
            name="My Favorite Rooms List", user=request.user
        )
        if action == "add":
            my_list.rooms.add(room)
        elif action == "remove":
            my_list.rooms.remove(room)
        # list_room = my_list.rooms.get_or_none(pk=room_pk)
        # if list_room is None:
        #     my_list.rooms.add(room)
        #     messages.success(request, "Favorite list added!!")
        # else:
        #     messages.warning(request, "This room exists!!")
        return redirect(reverse("rooms:detail", kwargs={"pk": room.pk}))
    return redirect(reverse("core:home"))


class FavListView(TemplateView):

    template_name = "lists/list_detail.html"
