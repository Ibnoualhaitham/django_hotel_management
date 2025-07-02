from django.db import models
from core.models import BaseMixin
from userApp.models import User
from .constants import HOTEL_STATUS_CHOICES, ROOM_TYPE_CHOICES, FACILITY_CHOICES


class Image(models.Model):
    image = models.ImageField(upload_to='assets/')

    def __str__(self):
        return f"Image {self.id}"


class Facility(models.Model):
    name = models.CharField(max_length=100, choices=FACILITY_CHOICES, unique=True)

    def __str__(self):
        return self.get_name_display()


class Hotel(BaseMixin):
    manager = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='managed_hotels')
    name = models.CharField(max_length=100)
    images = models.ManyToManyField(Image, blank=True, related_name='hotel_images')
    description = models.TextField(max_length=300)
    address = models.TextField(max_length=300)
    mobile = models.CharField(max_length=30)
    email = models.EmailField(max_length=80)
    status = models.CharField(max_length=30, choices=HOTEL_STATUS_CHOICES, default='available')
    facilities = models.ManyToManyField(Facility, blank=True)

    def __str__(self):
        return self.name


class Room(BaseMixin):
    room_number = models.IntegerField()
    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES, default='standard')
    images = models.ManyToManyField(Image, blank=True, related_name='room_images')
    is_available = models.BooleanField(default=True)
    price = models.FloatField(default=1000.00)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, null=True, blank=True, related_name='rooms')

    def __str__(self):
        return f"Room {self.room_number} ({self.room_type})"

    class Meta:
        unique_together = ('room_number', 'hotel')


class Location(BaseMixin):
    city = models.CharField(max_length=100)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, null=True, blank=True)
    latitude = models.DecimalField(max_digits=7, decimal_places=5)
    longitude = models.DecimalField(max_digits=7, decimal_places=5)

    def __str__(self):
        return self.city


class Review(BaseMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.TextField(max_length=200)
    star_rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=10.0,
        help_text="Rating between 0.0 and 10.0"
    )

    def __str__(self):
        username = self.user.username if self.user else 'Anonymous'
        return f"{self.star_rating} stars by {username}"
