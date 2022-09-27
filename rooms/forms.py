from pyexpat import model
from typing_extensions import Required
from django import forms
from django_countries.fields import CountryField

from rooms.admin import RoomAdmin
from . import models


class SearchForm(forms.Form):

    city = forms.CharField(initial="Anywhere")
    country = CountryField(default="KR").formfield()
    room_type = forms.ModelChoiceField(
        empty_label="Any Kind", queryset=models.RoomType.objects.all(), required=False
    )
    price = forms.IntegerField(required=False)
    guests = forms.IntegerField(required=False)
    bedrooms = forms.IntegerField(required=False)
    beds = forms.IntegerField(required=False)
    baths = forms.IntegerField(required=False)
    instant_book = forms.BooleanField(required=False)
    is_superhost = forms.BooleanField(required=False)
    amenities = forms.ModelMultipleChoiceField(
        queryset=models.Amenity.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    facilities = forms.ModelMultipleChoiceField(
        queryset=models.Facility.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    house_rules = forms.ModelMultipleChoiceField(
        queryset=models.HouseRule.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )


class CreateForm(forms.ModelForm):
    class Meta:
        model = models.Room
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

    def save(self, commit=False):
        room = super().save(commit)
        return room


class PhotoForm(forms.ModelForm):
    class Meta:
        model = models.Photo
        fields = [
            "file",
            "caption",
        ]

    def save(self, pk, commit=False):
        photo = super().save(commit)
        room = models.Room.objects.get(pk=pk)
        photo.room = room
        photo.save()
