from django.views.generic import ListView, DetailView
from django.shortcuts import render
from django_countries import countries
from . import models
from . import forms


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

    form = forms.SearchForm()

    return render(
        request,
        "rooms/search.html",
        {"form": form},
    )
