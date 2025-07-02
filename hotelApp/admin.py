from django.contrib import admin
from .models import Image, Room, Facility, Hotel, Location, Review


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image')
    search_fields = ('id',)
    ordering = ('id', 'image')


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'manager', 'status', 'mobile', 'email')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'manager__username', 'email')
    list_filter = ('status', 'facilities')
    filter_horizontal = ('facilities', 'images')
    autocomplete_fields = ['manager']
    ordering = ('name',)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'room_number', 'room_type', 'hotel', 'price', 'is_available',)
    list_display_links = ('id', 'hotel')
    list_filter = ('room_type', 'is_available', 'hotel')
    search_fields = ('room_number', 'hotel__name', 'price', 'is_available')
    autocomplete_fields = ['hotel']
    ordering = ('hotel', 'room_number', 'price')


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'city', 'hotel', 'latitude', 'longitude')
    search_fields = ('city', 'hotel__name')
    list_filter = ('city',)
    autocomplete_fields = ['hotel']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'hotel', 'star_rating', 'created_at')
    search_fields = ('user__username', 'hotel__name')
    list_filter = ('star_rating',)
    autocomplete_fields = ['user', 'hotel']
