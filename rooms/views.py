from django.views.generic import ListView, DetailView
from django.shortcuts import render
from django_countries import countries
from . import models


class HomeView(ListView):

    """HomeView Definition"""

    model = models.Room
    paginate_by = 10
    paginate_orphans = 5
    ordering = "-created_at"
    context_object_name = "rooms"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class RoomDetailView(DetailView):

    """RoomDetailView Denifition"""

    model = models.Room


def search(request):
    city = request.GET.get("city", "Anywhere")
    city = str.capitalize(city)
    country = request.GET.get("country", "KR")
    room_type = int(request.GET.get("room_type", 0))
    price = int(request.GET.get("price", 0))
    guests = int(request.GET.get("guests", 0))
    bedrooms = int(request.GET.get("bedrooms", 0))
    beds = int(request.GET.get("beds", 0))
    baths = int(request.GET.get("baths", 0))
    c_amenities = request.GET.getlist("amenities")
    c_facilities = request.GET.getlist("facilities")
    c_houserules = request.GET.getlist("houserules")
    c_instant = bool(request.GET.get("instant", False))
    c_super_host = bool(request.GET.get("super_host", False))

    form = {
        "s_city": city,
        "s_room_type": room_type,
        "s_country": country,
        "s_price": price,
        "s_guests": guests,
        "s_bedrooms": bedrooms,
        "s_beds": beds,
        "s_baths": baths,
        "s_amenities": c_amenities,
        "s_facilities": c_facilities,
        "s_houserules": c_houserules,
        "s_instant": c_instant,
        "s_super_host": c_super_host,
    }

    room_types = models.RoomType.objects.all()
    amenities = models.Amenity.objects.all()
    facilities = models.Facility.objects.all()
    houserules = models.HouseRule.objects.all()

    choices = {
        "countries": countries,
        "room_types": room_types,
        "amenities": amenities,
        "facilities": facilities,
        "houserules": houserules,
    }

    filter_args = {}

    if city != "Anywhere":
        filter_args["city__startswith"] = city

    filter_args["country"] = country

    if room_type != 0:
        filter_args["room_type__pk"] = room_type

    if price > 0:
        filter_args["price__lte"] = price

    if guests > 0:
        filter_args["price__lte"] = price

    if guests > 0:
        filter_args["guests__gte"] = guests

    if bedrooms > 0:
        filter_args["bedrooms__gte"] = bedrooms

    if beds > 0:
        filter_args["beds__gte"] = beds

    if baths > 0:
        filter_args["baths__gte"] = baths

    if c_instant is True:
        filter_args["instant_book"] = True

    if c_super_host is True:
        filter_args["host__is_superhost"] = True

    if len(c_amenities) > 0:
        for c_amenity in c_amenities:
            filter_args["amenities__pk"] = int(c_amenity)

    if len(c_facilities) > 0:
        for c_facility in c_facilities:
            filter_args["facilities__pk"] = int(c_facility)

    if len(c_houserules) > 0:
        for c_rule in c_houserules:
            filter_args["house_rules__pk"] = int(c_rule)

    rooms = models.Room.objects.filter(**filter_args)

    return render(
        request,
        "rooms/search.html",
        {**form, **choices, "rooms": rooms},
    )


# def room_detail(request, pk):
#     try:
#         room = models.Room.objects.get(pk=pk)
#         return render(request, "rooms/room_detail.html", {"room": room})
#     except models.Room.DoesNotExist:
#         raise Http404()


# def all_rooms(request):
#     page = request.GET.get("page", 1)
#     room_list = models.Room.objects.all()
#     paginator = Paginator(room_list, 10, orphans=5)
#     try:
#         rooms = paginator.page(int(page))
#         return render(request, "rooms/home.html", {"page": rooms})
#     except EmptyPage:
#         return redirect("/")
