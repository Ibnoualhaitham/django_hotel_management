from django.urls import path
from .views import (
    HotelListCreate,
    HotelRetrieveUpdateDestroy,
    RoomListCreate,
    RoomRetrieveUpdateDestroy,
    ReviewListCreate,
    ReviewRetrieveUpdateDestroy,
    BookingListCreate,
    BookingRetrieveUpdateDestroy,
    PaymentListCreate,
    PaymentRetrieveUpdateDestroy,
)

urlpatterns = [

    path('v2/hotels/', HotelListCreate.as_view(), name='hotel-list'),
    path('v2/hotels/<int:pk>/', HotelRetrieveUpdateDestroy.as_view(), name='hotel-detail'),

    path('v2/rooms/', RoomListCreate.as_view(), name='room-list'),
    path('v2/rooms/<int:pk>/', RoomRetrieveUpdateDestroy.as_view(), name='room-detail'),

    path('v2/reviews/', ReviewListCreate.as_view(), name='review-list'),
    path('v2/reviews/<int:pk>/', ReviewRetrieveUpdateDestroy.as_view(), name='review-detail'),

    path('v2/bookings/', BookingListCreate.as_view(), name='booking-list'),
    path('v2/bookings/<int:pk>/', BookingRetrieveUpdateDestroy.as_view(), name='booking-detail'),

    path('v2/payments/', PaymentListCreate.as_view(), name='payment-list'),
    path('v2/payments/<int:pk>/', PaymentRetrieveUpdateDestroy.as_view(), name='payment-detail'),
]
