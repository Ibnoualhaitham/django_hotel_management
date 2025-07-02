from django.urls import path
from django.views.generic import TemplateView

from .views import (
    RegistrationView, UserLoginView, UserLogoutView,
    UserProfileView,

    HotelListView, HotelDetailView, HotelCreateView, HotelUpdateView, HotelDeleteView,
    HotelBookView,

    RoomCreateView, RoomUpdateView, RoomDeleteView,

    BookingListView, BookingUpdateView, BookingDeleteView,
    PaymentCreateView,
)

urlpatterns = [

    path('register/', RegistrationView.as_view(), name='register'),
    path('', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),

    path('profile/', UserProfileView.as_view(), name='user_profile'),


    path('hotels/', HotelListView.as_view(), name='hotel_list'),
    path('hotels/create/', HotelCreateView.as_view(), name='hotel_create'),
    path('hotels/<int:pk>/', HotelDetailView.as_view(), name='hotel_detail'),
    path('hotels/<int:pk>/edit/', HotelUpdateView.as_view(), name='hotel_update'),
    path('hotels/<int:pk>/delete/', HotelDeleteView.as_view(), name='hotel_delete'),
    # path('hotels/<int:pk>/book/', HotelBookView.as_view(), name='book_hotel'),
    path('rooms/<int:pk>/book/', HotelBookView.as_view(), name='book_hotel'),


    path('hotels/<int:pk>/rooms/create/', RoomCreateView.as_view(), name='room_create'),
    path('rooms/<int:pk>/edit/', RoomUpdateView.as_view(), name='room_update'),
    path('rooms/<int:pk>/delete/', RoomDeleteView.as_view(), name='room_delete'),


    path('bookings/', BookingListView.as_view(), name='booking_list'),    
    path('bookings/<int:pk>/update/', BookingUpdateView.as_view(), name='booking_update'),
    path('bookings/<int:pk>/delete/', BookingDeleteView.as_view(), name='booking_delete'),


    path('bookings/<int:booking_id>/payment/', PaymentCreateView.as_view(), name='make_payment'),
    path('bookings/success/', TemplateView.as_view(template_name='booking_success.html'), name='booking_success'),
]
