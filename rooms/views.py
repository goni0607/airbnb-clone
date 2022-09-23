from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, View, UpdateView
from django.urls import reverse
from . import models, forms
from users import mixins


class HomeView(ListView):

    """HomeView Definition"""

    model = models.Room
    paginate_by = 12
    paginate_orphans = 5
    ordering = "-created_at"
    context_object_name = "rooms"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class RoomDetailView(DetailView):

    """RoomDetailView Denifition"""

    model = models.Room


class SearchView(View):
    def get(self, request):

        country = request.GET.get("country")

        if country:

            form = forms.SearchForm(request.GET)

            if form.is_valid():

                city = form.cleaned_data.get("city")
                country = form.cleaned_data.get("country")
                room_type = form.cleaned_data.get("room_type")
                price = form.cleaned_data.get("price")
                guests = form.cleaned_data.get("guests")
                bedrooms = form.cleaned_data.get("bedrooms")
                beds = form.cleaned_data.get("beds")
                baths = form.cleaned_data.get("baths")
                instant_book = form.cleaned_data.get("instant_book")
                is_superhost = form.cleaned_data.get("is_superhost")
                amenities = form.cleaned_data.get("amenities")
                facilities = form.cleaned_data.get("facilities")
                house_rules = form.cleaned_data.get("house_rules")

                filter_args = {}

                if city != "Anywhere":
                    filter_args["city__startswith"] = city

                filter_args["country"] = country

                if room_type is not None:
                    filter_args["room_type__pk"] = room_type

                if price is not None:
                    filter_args["price__lte"] = price

                if guests is not None:
                    filter_args["guests__gte"] = guests

                if bedrooms is not None:
                    filter_args["bedrooms__gte"] = bedrooms

                if beds is not None:
                    filter_args["beds__gte"] = beds

                if baths is not None:
                    filter_args["baths__gte"] = baths

                if instant_book is True:
                    filter_args["instant_book"] = True

                if is_superhost is True:
                    filter_args["host__superhost"] = True

                for amenity in amenities:
                    filter_args["amenities"] = amenity

                for facility in facilities:
                    filter_args["facilities"] = facility

                for rule in house_rules:
                    filter_args["house_rules"] = rule

                qs = models.Room.objects.filter(**filter_args).order_by("-created_at")

                paginator = Paginator(qs, 10, orphans=5)

                rooms = paginator.get_page(1)

                return render(
                    request,
                    "rooms/search.html",
                    {"form": form, "rooms": rooms},
                )
        else:

            form = forms.SearchForm()

        return render(request, "rooms/search.html", {"form": form})


class EditRoomView(mixins.LoggedInOnlyView, UpdateView):

    model = models.Room
    template_name = "rooms/room_edit.html"
    fields = [
        "name",
        "description",
        "country",
        "city",
        "price",
        "address",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
    ]

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room


class RoomPhotosView(mixins.LoggedInOnlyView, DetailView):

    model = models.Room
    template_name = "rooms/room_photos.html"

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room


@login_required
def delete_photo(request, room_pk, photo_pk):
    user = request.user
    try:
        room = models.Room.objects.get(pk=room_pk)
        if room.host.pk != user.pk:
            messages.error(request, "Can't delete that photo")
        else:
            try:
                photo = models.Photo.objects.get(pk=photo_pk, room__pk=room_pk)
                photo.delete()
                messages.success(request, "Photo deleted!!")
            except models.Photo.DoesNotExist:
                messages.error(request, "Can't delete that photo")
        return redirect(reverse("rooms:photos", kwargs={"pk": room_pk}))
    except models.Room.DoesNotExist:
        return redirect(reverse("core:home"))
