import datetime
from django.contrib import messages
from django.db.models.query import Q
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View
from . import models
from rooms import models as room_models


class CreateError(Exception):
    pass


def create(request, room, year, month, day):
    try:
        date_obj = datetime.datetime(year, month, day)
        print(date_obj)
        room = room_models.Room.objects.get(pk=room)
        print(room)
        room.reservations.get(check_in__lte=date_obj, check_out__gte=date_obj)
        raise CreateError()
    except (room_models.Room.DoesNotExist, CreateError):
        messages.error(request, "Can't Reserve That Room")
        return redirect(reverse("core:home"))
    except models.Reservation.DoesNotExist:
        reservation = models.Reservation.objects.create(
            check_in=date_obj,
            check_out=date_obj + datetime.timedelta(days=1),
            guest=request.user,
            room=room,
        )
        return redirect(reverse("reservations:detail", kwargs={"pk": reservation.pk}))


class DetailView(View):
    def get(self, request, pk):
        reservation = models.Reservation.objects.get_or_none(pk=pk)
        if not reservation:
            return redirect(reverse("core:home"))
