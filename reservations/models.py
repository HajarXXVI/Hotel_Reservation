from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.core.exceptions import ValidationError

class Hotel(models.Model):
    MOROCCAN_CITIES = [
        ('Marrakech', 'Marrakech'),
        ('Casablanca', 'Casablanca'),
        ('Rabat', 'Rabat'),
        ('Fes', 'Fes'),
        ('Tangier', 'Tangier'),
        ('Agadir', 'Agadir'),
        ('El Jadida', 'El Jadida'),
        ('Essaouira', 'Essaouira'),
        ('Chefchaouen', 'Chefchaouen'),
        ('M\'diq', 'M\'diq'),
        ('Ouarzazate', 'Ouarzazate'),
        ('Merzouga', 'Merzouga')
    ]

    HOTEL_AMENITIES = {
        'Free WiFi': {'type': 'basic', 'default_price': 0},
        'Swimming Pool': {'type': 'premium', 'default_price': 50},
        'Restaurant': {'type': 'dining', 'default_price': 0},
        'Spa': {'type': 'wellness', 'default_price': 100},
        'Fitness Center': {'type': 'wellness', 'default_price': 30},
        'Room Service': {'type': 'service', 'default_price': 0},
        'Bar/Lounge': {'type': 'dining', 'default_price': 0},
        'Airport Shuttle': {'type': 'transport', 'default_price': 75},
        'Parking': {'type': 'transport', 'default_price': 20},
        'Business Center': {'type': 'business', 'default_price': 25},
        'Conference Rooms': {'type': 'business', 'default_price': 200},
        'Kids Club': {'type': 'family', 'default_price': 40},
        'Beach Access': {'type': 'location', 'default_price': 0},
        'Garden': {'type': 'outdoor', 'default_price': 0},
        'Terrace': {'type': 'outdoor', 'default_price': 0}
    }

    name = models.CharField(_('name'), max_length=200)
    address = models.TextField(_('address'))
    city = models.CharField(_('city'), max_length=100, choices=MOROCCAN_CITIES)
    description = models.TextField(
        _('description'),
        help_text=_('Detailed description of the hotel, including its history, style, and unique features.')
    )
    amenities = models.JSONField(
        _('amenities'), 
        default=list,
        help_text=_('Select amenities for this hotel. Some amenities have additional charges.')
    )
    rating = models.DecimalField(
        _('rating'),
        max_digits=3,
        decimal_places=1,
        null=True,
        blank=True,
        help_text=_('Rating from 0.0 to 5.0')
    )
    main_photo = models.ImageField(_('main photo'), upload_to='hotel_photos/', null=True, blank=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('hotel')
        verbose_name_plural = _('hotels')

    def __str__(self):
        return f"{self.name} - {self.city}"

    def clean(self):
        if self.rating and (self.rating < 0 or self.rating > 5):
            raise ValidationError({
                'rating': _('Rating must be between 0 and 5')
            })

    def get_amenity_price(self, amenity_name):
        """Get the price for a specific amenity."""
        if amenity_name in self.HOTEL_AMENITIES:
            return self.HOTEL_AMENITIES[amenity_name]['default_price']
        return None

    def get_amenities_by_type(self):
        """Group amenities by their type."""
        grouped = {}
        for amenity in self.amenities:
            if amenity in self.HOTEL_AMENITIES:
                amenity_type = self.HOTEL_AMENITIES[amenity]['type']
                if amenity_type not in grouped:
                    grouped[amenity_type] = []
                grouped[amenity_type].append({
                    'name': amenity,
                    'price': self.get_amenity_price(amenity)
                })
        return grouped

class HotelPhoto(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='photos')
    photo = models.ImageField(upload_to='hotel_photos/')
    caption = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = _('hotel photo')
        verbose_name_plural = _('hotel photos')
        ordering = ['order']

    def __str__(self):
        return f"Photo for {self.hotel.name}"

class Room(models.Model):
    ROOM_TYPES = [
        ('single', _('Single')),
        ('double', _('Double')),
        ('suite', _('Suite')),
        ('family', _('Family')),
        ('deluxe', _('Deluxe')),
    ]

    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        related_name='rooms',
        verbose_name=_('hotel'),
        null=True,
        blank=True
    )
    room_number = models.CharField(_('room number'), max_length=10)
    room_type = models.CharField(_('room type'), max_length=20, choices=ROOM_TYPES)
    price_per_night = models.DecimalField(
        _('price per night'),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    is_available = models.BooleanField(_('is available'), default=True)
    photo = models.ImageField(_('photo'), upload_to='room_photos/', null=True, blank=True)

    class Meta:
        verbose_name = _('room')
        verbose_name_plural = _('rooms')
        unique_together = ['hotel', 'room_number']

    def __str__(self):
        return f"{self.hotel.name} - Room {self.room_number} ({self.get_room_type_display()})"

class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('confirmed', _('Confirmed')),
        ('cancelled', _('Cancelled')),
        ('completed', _('Completed')),
    ]

    PAYMENT_STATUS = [
        ('pending', _('Pending')),
        ('partial', _('Partial')),
        ('paid', _('Paid')),
        ('refunded', _('Refunded')),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reservations'
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='reservations'
    )
    check_in_date = models.DateField(_('check-in date'))
    check_out_date = models.DateField(_('check-out date'))
    number_of_guests = models.PositiveIntegerField(_('number of guests'))
    total_price = models.DecimalField(_('total price'), max_digits=10, decimal_places=2)
    selected_amenities = models.JSONField(_('selected amenities'), default=list)
    amenities_total_price = models.DecimalField(_('amenities total price'), max_digits=10, decimal_places=2, default=Decimal('0.00'))
    status = models.CharField(
        _('status'),
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    payment_status = models.CharField(
        _('payment status'),
        max_length=20,
        choices=PAYMENT_STATUS,
        default='pending'
    )
    special_requests = models.TextField(_('special requests'), blank=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('reservation')
        verbose_name_plural = _('reservations')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.get_full_name()} - Room {self.room.room_number} ({self.check_in_date} to {self.check_out_date})"

    def calculate_number_of_days(self):
        """Calculate the number of days between check-in and check-out."""
        if self.check_in_date and self.check_out_date:
            return (self.check_out_date - self.check_in_date).days
        return 0

    def calculate_room_price(self):
        """Calculate the total room price based on number of days."""
        days = self.calculate_number_of_days()
        return self.room.price_per_night * days

    def calculate_amenities_price(self):
        """Calculate the total price of selected amenities."""
        total = Decimal('0.00')
        if not self.selected_amenities:
            return total
        
        hotel_amenities = self.room.hotel.HOTEL_AMENITIES
        for amenity in self.selected_amenities:
            if amenity in hotel_amenities:
                total += Decimal(str(hotel_amenities[amenity]['default_price']))
        return total

    def calculate_total_price(self):
        """Calculate the total price including room and amenities."""
        room_price = self.calculate_room_price()
        amenities_price = self.calculate_amenities_price()
        return room_price + amenities_price

    def save(self, *args, **kwargs):
        """Override save to automatically calculate prices."""
        if self.check_in_date and self.check_out_date and self.room:
            self.amenities_total_price = self.calculate_amenities_price()
            self.total_price = self.calculate_total_price()
        super().save(*args, **kwargs)

class Review(models.Model):
    reservation = models.OneToOneField(
        Reservation,
        on_delete=models.CASCADE,
        related_name='review'
    )
    rating = models.PositiveIntegerField(
        _('rating'),
        validators=[MinValueValidator(1)]
    )
    comment = models.TextField(_('comment'))
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('review')
        verbose_name_plural = _('reviews')
        ordering = ['-created_at']

    def __str__(self):
        return f"Review by {self.reservation.user.get_full_name()} for Room {self.reservation.room.room_number}"
