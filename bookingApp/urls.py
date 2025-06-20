from django.urls import path
from django.views.generic import TemplateView

from .views import (
    RegistrationView, UserLoginView, UserLogoutView,
    UserProfileView,

    # Hotel-related views
    HotelListView, HotelDetailView, HotelCreateView, HotelUpdateView, HotelDeleteView,
    HotelBookView,

    # Room-related views
    RoomCreateView, RoomUpdateView, RoomDeleteView,

    # Booking and Payment views
    BookingView, BookingListView, BookingUpdateView, BookingDeleteView,
    PaymentCreateView,
)

urlpatterns = [
    # 🔐 Authentication
    path('register/', RegistrationView.as_view(), name='register'),
    path('', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),

    # 👤 User Profile
    path('profile/', UserProfileView.as_view(), name='user_profile'),

    # 🏨 Hotel URLs
    path('hotels/', HotelListView.as_view(), name='hotel_list'),
    path('hotels/create/', HotelCreateView.as_view(), name='hotel_create'),
    path('hotels/<int:pk>/', HotelDetailView.as_view(), name='hotel_detail'),
    path('hotels/<int:pk>/edit/', HotelUpdateView.as_view(), name='hotel_update'),
    path('hotels/<int:pk>/delete/', HotelDeleteView.as_view(), name='hotel_delete'),
    path('hotels/<int:pk>/book/', HotelBookView.as_view(), name='book_hotel'),
    path('rooms/<int:pk>/book/', HotelBookView.as_view(), name='book_hotel'),

    # 🚪 Room URLs
    path('hotels/<int:pk>/rooms/create/', RoomCreateView.as_view(), name='room_create'),
    path('rooms/<int:pk>/edit/', RoomUpdateView.as_view(), name='room_update'),
    path('rooms/<int:pk>/delete/', RoomDeleteView.as_view(), name='room_delete'),

    # 📅 Bookings
    path('bookings/', BookingListView.as_view(), name='booking_list'),
    path('bookings/new/<int:hotel_id>/<int:room_id>/', BookingView.as_view(), name='book_room'),
    

    path('bookings/<int:pk>/update/', BookingUpdateView.as_view(), name='booking_update'),
    path('bookings/<int:pk>/delete/', BookingDeleteView.as_view(), name='booking_delete'),

    # 💳 Payments
    path('bookings/<int:booking_id>/payment/', PaymentCreateView.as_view(), name='make_payment'),
    path('bookings/success/', TemplateView.as_view(template_name='booking_success.html'), name='booking_success'),
]
