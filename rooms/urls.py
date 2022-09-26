from django.urls import path
from . import views

app_name = "rooms"

urlpatterns = [
    path("<int:pk>/", views.RoomDetailView.as_view(), name="detail"),
    path("search/", views.SearchView.as_view(), name="search"),
    path("<int:pk>/edit/", views.EditRoomView.as_view(), name="edit"),
    path("<int:pk>/photos/", views.RoomPhotosView.as_view(), name="photos"),
    path("<int:pk>/photos/add/", views.CreatePhotoView.as_view(), name="add-photo"),
    path(
        "<int:room_pk>/photos/<int:photo_pk>/delete/",
        views.delete_photo,
        name="photo-delete",
    ),
    path(
        "<int:room_pk>/photos/<int:photo_pk>/edit/",
        views.EditPhotoView.as_view(),
        name="photo-edit",
    ),
]
