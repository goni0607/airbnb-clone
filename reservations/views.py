import datetime
from django.contrib import messages
from django.db.models.query import Q
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View
from . import models
from reviews import forms as review_forms
from rooms import models as room_models


class CreateError(Exception):
    pass


def create(request, room, year, month, day):
    try:
        date_obj = datetime.datetime(year, month, day)
        print(date_obj)
        room = room_models.Room.objects.get(pk=room)
        print(room)
        room.reservations.get(
            Q(check_in__lte=date_obj, check_out__gte=date_obj) & ~Q(status="canceled")
        )
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
        print(reservation)
        if not reservation:
            print("404")
            raise Http404()

        print(reservation.guest, request.user)
        if reservation.guest != request.user and reservation.room.host != request.user:
            raise Http404()
        form = review_forms.CreateReviewForm()
        return render(
            request,
            "reservations/detail.html",
            {"reservation": reservation, "review_form": form},
        )


def edit_reservation(request, pk, verb):
    reservation = models.Reservation.objects.get_or_none(pk=pk)
    if not reservation or (
        reservation.guest != request.user and reservation.room.host != request.user
    ):
        raise Http404()
    if verb == "confirm":
        reservation.status = models.Reservation.STATUS_CONFIRMED
    elif verb == "cancel":
        reservation.status = models.Reservation.STATUS_CANCELED

    reservation.save()
    messages.success(request, "Reservation UPdated!!")
    return redirect(reverse("reservations:detail", kwargs={"pk": reservation.pk}))
