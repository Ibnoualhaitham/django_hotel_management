# bookingApp/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from userApp.models import User
from .models import Booking, Payment


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': 'Username',
            'email': 'Email Address',
            'password1': 'Password',
            'password2': 'Confirm Password',
        }


class BookingForm(forms.ModelForm):
    check_in_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Check-in Date'
    )
    check_out_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Check-out Date'
    )

    class Meta:
        model = Booking
        fields = ['room', 'check_in_date', 'check_out_date', 'number_of_persons']
        labels = {
            'room': 'Select Room',
            'number_of_persons': 'Number of Guests',
        }


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount_paid', 'payment_status', 'payment_method', 'transaction_id']
        labels = {
            'amount_paid': 'Amount Paid',
            'payment_status': 'Payment Status',
            'payment_method': 'Payment Method',
            'transaction_id': 'Transaction ID',
        }
