from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (
    CreateView, TemplateView, ListView, DetailView, UpdateView, DeleteView
)
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from .models import Booking, Payment
from hotelApp.models import Hotel, Review, Room, Image  # include Image model
from .forms import RegisterForm, BookingForm, PaymentForm


# --- User Management ---
class RegistrationView(CreateView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('user_profile')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        auth_login(self.request, user)
        messages.success(self.request, 'Registration successful!')
        return redirect(self.success_url)


class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'login.html'
    form_class = AuthenticationForm
    success_message = 'Login successful!'

    def get_success_url(self):
        return reverse_lazy('user_profile')


class UserLogoutView(LoginRequiredMixin, LogoutView):
    next_page = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, 'Logout successful!')
        return super().dispatch(request, *args, **kwargs)


class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'user_profile.html'


# --- Hotel Views ---
class HotelListView(LoginRequiredMixin, ListView):
    model = Hotel
    template_name = 'hotel_list.html'
    context_object_name = 'hotels'


class HotelDetailView(LoginRequiredMixin, DetailView):
    model = Hotel
    template_name = 'hotel_detail.html'
    context_object_name = 'hotel'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = Review.objects.filter(hotel=self.object)
        return context


class HotelCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Hotel
    fields = ['name', 'description', 'images', 'address', 'mobile', 'email', 'status', 'facilities', 'manager']
    template_name = 'hotel_form.html'
    success_url = reverse_lazy('hotel_list')
    success_message = 'Hotel Created Successfully'


class HotelUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Hotel
    fields = ['name', 'description', 'address', 'mobile', 'email', 'status', 'facilities', 'manager']
    template_name = 'hotel_form.html'
    success_url = reverse_lazy('hotel_list')
    success_message = "Hotel updated successfully."

    def form_valid(self, form):
        response = super().form_valid(form)

        # Optional: clear existing images if replacing them
        # self.object.images.clear()

        for image_file in self.request.FILES.getlist('images'):
            img = Image.objects.create(image=image_file)
            self.object.images.add(img)

        return response
    
class HotelDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Hotel
    template_name = 'hotel_confirm_delete.html'
    success_url = reverse_lazy('hotel_list')
    success_message = "Hotel deleted successfully."


# --- Booking and Payment ---
class HotelBookView(LoginRequiredMixin, CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'book_hotel.html'

    def dispatch(self, request, *args, **kwargs):
        self.hotel = get_object_or_404(Hotel, pk=kwargs['pk'])
        if self.hotel.status in ['booked', 'closed']:
            messages.error(request, "This hotel is not available for booking.")
            return redirect('hotel_detail', pk=self.hotel.pk)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.hotel = self.hotel
        form.instance.status = 'pending'
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hotel'] = self.hotel
        return context

    def get_success_url(self):
        return reverse_lazy('make_payment', kwargs={'booking_id': self.object.pk})


# --- Book a Room (HotelBookView expects to book a specific room) ---
class HotelBookView(LoginRequiredMixin, CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'book_hotel.html'

    def dispatch(self, request, *args, **kwargs):
        self.room = get_object_or_404(Room, pk=kwargs['pk'])
        if not self.room.is_available:
            messages.error(request, "This room is not available for booking.")
            return redirect('hotel_detail', pk=self.room.hotel.pk)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.room = self.room
        form.instance.is_active = True  # Default to active when created
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['room'] = self.room
        context['hotel'] = self.room.hotel
        return context

    def get_success_url(self):
        return reverse_lazy('make_payment', kwargs={'booking_id': self.object.pk})


# --- Create Booking (General) ---
class BookingView(LoginRequiredMixin, CreateView):
    form_class = BookingForm
    template_name = 'booking_form.html'
    success_url = reverse_lazy('user_profile')

    def dispatch(self, request, *args, **kwargs):
        self.hotel = get_object_or_404(Hotel, pk=self.kwargs['hotel_id'])
        self.room = get_object_or_404(Room, pk=self.kwargs['room_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.hotel = self.hotel
        form.instance.room = self.room
        messages.success(self.request, 'Booking created successfully!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hotel'] = self.hotel
        context['room'] = self.room
        return context



# --- List Bookings ---
class BookingListView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'booking_list.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)


class BookingUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Booking
    form_class = BookingForm
    template_name = 'booking_form.html'
    success_message = "Booking updated successfully."

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('booking_list')


# --- Delete Booking ---
class BookingDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Booking
    template_name = 'room_confirm_delete.html'
    success_message = "Booking deleted successfully."

    def get_queryset(self):
        # Only allow users to delete their own bookings
        return Booking.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('booking_list')



class PaymentCreateView(LoginRequiredMixin, CreateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'payment_form.html'
    success_url = reverse_lazy('booking_success')

    def dispatch(self, request, *args, **kwargs):
        self.booking = get_object_or_404(Booking, pk=kwargs['booking_id'], user=request.user)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.booking = self.booking
        messages.success(self.request, 'Payment completed successfully!')
        return super().form_valid(form)


# --- Room Views ---
class RoomCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Room
    fields = ['room_number', 'room_type', 'is_available', 'price']
    template_name = 'room_form.html'
    success_message = 'Room created successfully.'

    def dispatch(self, request, *args, **kwargs):
        self.hotel = get_object_or_404(Hotel, pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.hotel = self.hotel
        response = super().form_valid(form)

        # Save uploaded images
        for image_file in self.request.FILES.getlist('images'):
            img = Image.objects.create(image=image_file)
            self.object.images.add(img)

        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hotel_object'] = self.hotel
        return context

    def get_success_url(self):
        return reverse_lazy('hotel_detail', kwargs={'pk': self.hotel.pk})


class RoomUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Room
    fields = ['room_number', 'room_type', 'is_available', 'price']  # do not include images here
    template_name = 'room_form.html'
    success_message = "Room updated successfully."

    def form_valid(self, form):
        # Save the basic room data
        response = super().form_valid(form)

        # Optional: Clear old images if you want to replace them
        self.object.images.clear()

        # Add new uploaded images
        for image_file in self.request.FILES.getlist('images'):
            img = Image.objects.create(image=image_file)
            self.object.images.add(img)

        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hotel_object'] = self.object.hotel
        return context

    def get_success_url(self):
        return reverse_lazy('hotel_detail', kwargs={'pk': self.object.hotel.pk})

class RoomDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Room
    template_name = 'room_confirm_delete.html'
    success_message = "Room deleted successfully."

    def get_success_url(self):
        hotel = self.get_object().hotel
        return reverse_lazy('hotel_detail', kwargs={'pk': hotel.pk})
