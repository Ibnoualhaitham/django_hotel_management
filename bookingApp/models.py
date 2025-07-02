from django.db import models
from userApp.models import User
from hotelApp.models import Room
from .constants import PAYMENT_STATUS, PAYMENT_METHOD



class BookingQuerySet(models.QuerySet):
    def for_manager(self, manager_user):
        return self.filter(room__hotel__manager=manager_user)


class PaymentQuerySet(models.QuerySet):
    def for_manager(self, manager_user):
        return self.filter(booking__room__hotel__manager=manager_user)


class BookingManager(models.Manager):
    def get_queryset(self):
        return BookingQuerySet(self.model, using=self._db)

    def for_manager(self, manager_user):
        return self.get_queryset().for_manager(manager_user)


class PaymentManager(models.Manager):
    def get_queryset(self):
        return PaymentQuerySet(self.model, using=self._db)

    def for_manager(self, manager_user):
        return self.get_queryset().for_manager(manager_user)


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1,  related_name='bookings')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    number_of_persons = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    booked_on = models.DateTimeField(auto_now_add=True)

    objects = BookingManager()

    def __str__(self):
        return f"Booking by {self.user.username} in Room {self.room.room_number} at {self.room.hotel.name}"


class Payment(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='payments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    amount_paid = models.FloatField()
    payment_status = models.CharField(max_length=30, choices=PAYMENT_STATUS, default='pending')
    payment_method = models.CharField(max_length=30, choices=PAYMENT_METHOD, default='credit_card')
    transaction_id = models.CharField(max_length=12, unique=True)

    objects = PaymentManager()

    def __str__(self):
        return f"₹{self.amount_paid} by {self.user.username}"
