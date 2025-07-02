from django.contrib import admin
from .models import Booking, Payment


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'room', 'check_in_date', 'check_out_date',
        'number_of_persons', 'is_active', 'booked_on'
    )
    list_filter = ('is_active', 'booked_on', 'check_in_date', 'check_out_date')
    search_fields = ('user__username', 'room__room_number', 'room__hotel__name')
    ordering = ('-booked_on',)
    date_hierarchy = 'check_in_date'
    autocomplete_fields = ['user', 'room']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'booking', 'user', 'amount_paid', 'payment_status',
        'payment_method', 'transaction_id'
    )
    list_filter = ('payment_status', 'payment_method')
    search_fields = ('user__username', 'transaction_id', 'booking__id')
    ordering = ('-id',)
    autocomplete_fields = ['user', 'booking']
