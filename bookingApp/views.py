from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, TemplateView, ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from .models import Booking, Payment
from hotelApp.models import Hotel, Review, Room, Image
from bookingApp.forms import RegisterForm, BookingForm, PaymentForm
from hotelApp.forms import HotelForm, RoomForm, ReviewForm
from userApp.models import User
from core.models import BaseMixin



class RegistrationView(SuccessMessageMixin, BaseMixin, CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')
    success_message = 'Registration successful!'


class UserLoginView(BaseMixin, LoginView):
    template_name = 'login.html'
    form_class = AuthenticationForm

    def get_success_url(self):
        return reverse_lazy('user_profile')


class UserLogoutView(BaseMixin, LogoutView):
    next_page = reverse_lazy('login')
    success_message = 'logout successfully!'


class UserProfileView(LoginRequiredMixin, BaseMixin, TemplateView):
    template_name = 'user_profile.html'



class HotelListView(LoginRequiredMixin, BaseMixin, ListView):
    model = Hotel
    template_name = 'hotel_list.html'
    context_object_name = 'hotels'
    login_url = reverse_lazy('login')


class HotelDetailView(LoginRequiredMixin, BaseMixin, DetailView):
    model = Hotel
    template_name = 'hotel_detail.html'
    context_object_name = 'hotel'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = Review.objects.filter(hotel=self.object)
        return context


class HotelCreateView(LoginRequiredMixin, BaseMixin, SuccessMessageMixin, CreateView):
    model = Hotel
    form_class = HotelForm
    template_name = 'hotel_form.html'
    success_url = reverse_lazy('hotel_list')
    success_message = 'Hotel created successfully.'

    def form_valid(self, form):
        form.instance.manager = self.request.user
        response = super().form_valid(form)

        for file in self.request.FILES.getlist('images'):
            image = Image.objects.create(image=file)
            form.instance.images.add(image)

        return response


class HotelUpdateView(LoginRequiredMixin, BaseMixin, SuccessMessageMixin, UpdateView):
    model = Hotel
    form_class = HotelForm
    template_name = 'hotel_form.html'
    success_url = reverse_lazy('hotel_list')
    success_message = "Hotel updated successfully."

    def form_valid(self, form):
        response = super().form_valid(form)

        delete_ids = self.request.POST.getlist('delete_images')
        if delete_ids:
            for image_id in delete_ids:
                try:
                    img = Image.objects.get(id=image_id)
                    form.instance.images.remove(img)
                except Image.DoesNotExist:
                    continue

        for file in self.request.FILES.getlist('images'):
            image = Image.objects.create(image=file)
            form.instance.images.add(image)

        return response


class HotelDeleteView(LoginRequiredMixin, BaseMixin, SuccessMessageMixin, DeleteView):
    model = Hotel
    template_name = 'hotel_confirm_delete.html'
    success_url = reverse_lazy('hotel_list')
    success_message = "Hotel deleted successfully."


class RoomCreateView(LoginRequiredMixin, BaseMixin, SuccessMessageMixin, CreateView):
    model = Room
    fields = ['room_number', 'room_type', 'is_available', 'price',]
    template_name = 'room_form.html'
    success_message = 'Room created successfully.'

    def get(self, request, *args, **kwargs):
        self.hotel = get_object_or_404(Hotel, id=kwargs['pk'])
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.hotel = get_object_or_404(Hotel, id=kwargs['pk'])
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.hotel = self.hotel
        response = super().form_valid(form)

        for file in self.request.FILES.getlist('images'):
            image = Image.objects.create(image=file)
            form.instance.images.add(image)

        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hotel_object'] = self.hotel
        return context

    def get_success_url(self):
        return reverse_lazy('hotel_detail', kwargs={'pk': self.hotel.id})


class RoomUpdateView(LoginRequiredMixin, BaseMixin, SuccessMessageMixin, UpdateView):
    model = Room
    form_class = RoomForm
    template_name = 'room_form.html'
    success_message = "Room updated successfully."

    def form_valid(self, form):
        response = super().form_valid(form)

        delete_ids = self.request.POST.getlist('delete_images')
        if delete_ids:
            for image_id in delete_ids:
                try:
                    img = Image.objects.get(id=image_id)
                    form.instance.images.remove(img)
                except Image.DoesNotExist:
                    continue

        for file in self.request.FILES.getlist('images'):
            image = Image.objects.create(image=file)
            form.instance.images.add(image)

        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hotel_object'] = self.object.hotel
        return context

    def get_success_url(self):
        return reverse_lazy('hotel_detail', kwargs={'pk': self.object.hotel.pk})


class RoomDeleteView(LoginRequiredMixin, BaseMixin, SuccessMessageMixin, DeleteView):
    model = Room
    template_name = 'room_confirm_delete.html'
    success_message = "Room deleted successfully."

    def get_success_url(self):
        hotel = self.get_object().hotel
        return reverse_lazy('hotel_detail', kwargs={'pk': hotel.pk})


# Booking & Payment 

class HotelBookView(LoginRequiredMixin, BaseMixin, CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'book_hotel.html'

    def form_valid(self, form):
        room = get_object_or_404(Room, pk=self.kwargs['pk'])
        if not room.is_available:
            messages.error(self.request, "This room is not available for booking.")
            return redirect('hotel_detail', pk=room.hotel.pk)
        
        form.instance.user = self.request.user
        form.instance.room = room
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = get_object_or_404(Room, pk=self.kwargs['pk'])
        context['room'] = room
        context['hotel'] = room.hotel
        return context

    def get_success_url(self):
        return reverse_lazy('make_payment', kwargs={'booking_id': self.object.pk})



class BookingListView(LoginRequiredMixin, BaseMixin, ListView):
    model = Booking
    template_name = 'booking_list.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)


class BookingUpdateView(LoginRequiredMixin, BaseMixin, SuccessMessageMixin, UpdateView):
    model = Booking
    form_class = BookingForm
    template_name = 'booking_form.html'
    success_message = "Booking updated successfully."

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('booking_list')


class BookingDeleteView(LoginRequiredMixin, BaseMixin, SuccessMessageMixin, DeleteView):
    model = Booking
    template_name = 'room_confirm_delete.html'
    success_message = "Booking deleted successfully."

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('booking_list')


class PaymentCreateView(LoginRequiredMixin, BaseMixin, CreateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'payment_form.html'
    success_url = reverse_lazy('booking_success')

    def get(self, request, *args, **kwargs):
        self.booking = get_object_or_404(Booking, pk=kwargs['booking_id'], user=self.request.user)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.booking = get_object_or_404(Booking, pk=kwargs['booking_id'], user=self.request.user)
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.booking = self.booking
        messages.success(self.request, 'Payment completed successfully!')
        return super().form_valid(form)
