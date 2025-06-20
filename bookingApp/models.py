from django.db import models
from django.core.exceptions import ValidationError
from userApp.models import User
from hotelApp.models import Room

# --- Constants ---
PAYMENT_STATUS = (
    ('paid', 'Paid'),
    ('pending', 'Pending'),
    ('canceled', 'Canceled'),
    ('unpaid', 'Unpaid'),
)

PAYMENT_METHOD = (
    ('credit_card', 'Credit Card'),
    ('debit_card', 'Debit Card'),
    ('upi', 'UPI'),
    ('paypal', 'PayPal'),
)


# --- Booking Model ---
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings', null=True, blank=True)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    number_of_persons = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    booked_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking by {self.user.username} in Room {self.room.room_number} at {self.room.hotel.name}"

    def clean(self):
        """
        Prevent double booking of the same room for overlapping dates.
        """
        overlapping = Booking.objects.filter(
            room=self.room,
            check_in_date__lt=self.check_out_date,
            check_out_date__gt=self.check_in_date,
            is_active=True
        )
        if self.pk:
            overlapping = overlapping.exclude(pk=self.pk)

        if overlapping.exists():
            raise ValidationError(
                f"Room {self.room.room_number} is already booked for the selected dates."
            )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    @classmethod
    def for_manager(cls, manager_user):
        """
        Return all bookings for rooms in hotels managed by this manager.
        """
        return cls.objects.filter(room__hotel__manager=manager_user)


# --- Payment Model ---
class Payment(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='payments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    amount_paid = models.FloatField()
    payment_status = models.CharField(max_length=30, choices=PAYMENT_STATUS, default='pending')
    payment_method = models.CharField(max_length=30, choices=PAYMENT_METHOD, default='credit_card')
    transaction_id = models.CharField(max_length=12, unique=True)

    def __str__(self):
        return f"₹{self.amount_paid} by {self.user.username}"

    @classmethod
    def for_manager(cls, manager_user):
        """
        Return all payments for bookings related to hotels managed by this manager.
        """
        return cls.objects.filter(booking__room__hotel__manager=manager_user)
