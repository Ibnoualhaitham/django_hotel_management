from django import forms
from .models import Room, Hotel, Facility, Location, Review, Image


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']


class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ['manager', 'name', 'description', 'address', 'mobile', 'email', 'status', 'facilities',]

        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'address': forms.Textarea(attrs={'rows': 2}),
        }


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_number', 'room_type', 'is_available', 'price', 'hotel',]


class FacilityForm(forms.ModelForm):
    class Meta:
        model = Facility
        fields = ['name']


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['city', 'hotel', 'latitude', 'longitude']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['user', 'hotel', 'comment', 'star_rating']
