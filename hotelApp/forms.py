from django import forms
from .models import Room, Hotel, Facility, Location, Review, Image


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_number', 'room_type', 'images', 'is_available', 'price']


class FacilityForm(forms.ModelForm):
    class Meta:
        model = Facility
        fields = ['name']  # 'name' uses choices, no need to define all options manually


class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = [
            'manager',
            'name',
            'images',
            'description',
            'address',
            'mobile',
            'email',
            'status',
            'facilities',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'address': forms.Textarea(attrs={'rows': 2}),
        }


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['city', 'hotel', 'latitude', 'longitude']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['user', 'hotel', 'comment', 'star_rating']


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']  # Correct field name is 'image'
