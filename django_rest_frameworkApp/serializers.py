from rest_framework import serializers
from bookingApp.models import Booking, Payment
from hotelApp.models import Hotel, Room, Review, Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image    
        fields = ['id', 'image']



class HotelSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Hotel
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    hotel_name = serializers.CharField(source='hotel.name', read_only=True)

    class Meta:
        model = Room
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    hotel_name = serializers.CharField(source='hotel.name', read_only=True)

    class Meta:
        model = Review 
        fields = '__all__'

    def validate_star_rating(self, value):
        if not 0.0 <= value <= 10.0:
            raise serializers.ValidationError("Rating must be between 0.0 and 10.0")
        return value



from datetime import date
from bookingApp.models import Booking

class BookingSerializer(serializers.ModelSerializer):
    room_number = serializers.IntegerField(source='room.room_number', read_only=True)
    hotel_name = serializers.CharField(source='room.hotel.name', read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = '__all__'

    def validate(self, data):
        room = data['room']
        check_in = data['check_in_date']
        check_out = data['check_out_date']

        if check_in >= check_out:
            raise serializers.ValidationError("Check-out must be after check-in.")
        if check_in < date.today():
            raise serializers.ValidationError("Check-in date cannot be in the past.")

        overlapping = Booking.objects.filter(
            room=room,
            check_in_date__lt=check_out,
            check_out_date__gt=check_in,
            is_active=True
        )
        if self.instance:
            overlapping = overlapping.exclude(pk=self.instance.pk)
        if overlapping.exists():
            raise serializers.ValidationError("Room is already booked for the selected dates.")

        return data

    def get_total_price(self, obj):
        days = (obj.check_out_date - obj.check_in_date).days
        return days * obj.room.price



class PaymentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    booking_info = serializers.StringRelatedField(source='booking', read_only=True)

    class Meta:
        model = Payment
        fields = '__all__'

    def validate_amount_paid(self, value):
        if value <= 0:
            raise serializers.ValidationError("Payment amount must be positive.")
        return value

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            validated_data['user'] = request.user
        return super().create(validated_data)
