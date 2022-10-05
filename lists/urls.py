from django.urls import path
from . import views

app_name = "lists"

urlpatterns = [
    path("toggle/<int:room_pk>/", views.toggle_view, name="toggle"),
    path("favs/", views.FavListView.as_view(), name="favs"),
]
