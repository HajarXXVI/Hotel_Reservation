from django import forms
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Hotel, HotelPhoto, Room, Reservation, Review

class HotelAdminForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = '__all__'
        widgets = {
            'amenities': forms.CheckboxSelectMultiple(
                choices=[(k, f"{k} ({v['type']}{' - ' + str(v['default_price']) + ' MAD' if v['default_price'] > 0 else ''})") 
                        for k, v in Hotel.HOTEL_AMENITIES.items()]
            )
        }

class HotelPhotoInline(admin.TabularInline):
    model = HotelPhoto
    extra = 1
    fields = ('photo', 'caption', 'is_primary', 'order')

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    form = HotelAdminForm
    list_display = ('name', 'city', 'rating', 'get_amenities_count')
    list_filter = ('city', 'rating')
    search_fields = ('name', 'address', 'city')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [HotelPhotoInline]
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'rating', 'main_photo')
        }),
        (_('Location'), {
            'fields': ('address', 'city')
        }),
        (_('Amenities'), {
            'fields': ('amenities',),
            'description': _('Select amenities for this hotel. Items marked with a price will be charged extra.')
        }),
        (_('Additional Information'), {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def get_amenities_count(self, obj):
        return len(obj.amenities) if obj.amenities else 0
    get_amenities_count.short_description = _('Amenities Count')

@admin.register(HotelPhoto)
class HotelPhotoAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'caption', 'is_primary', 'order')
    list_filter = ('hotel', 'is_primary')
    search_fields = ('hotel__name', 'caption')
    ordering = ('hotel', 'order')

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'room_number', 'room_type', 'price_per_night', 'is_available')
    list_filter = ('hotel', 'room_type', 'is_available')
    search_fields = ('room_number', 'hotel__name')
    fieldsets = (
        (None, {
            'fields': ('hotel', 'room_number', 'room_type', 'price_per_night')
        }),
        (_('Room Details'), {
            'fields': ('is_available', 'photo')
        }),
    )

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'check_in_date', 'check_out_date', 'get_number_of_days', 
                   'get_room_price', 'get_amenities_price', 'total_price', 'status', 'payment_status')
    list_filter = ('status', 'payment_status', 'check_in_date', 'check_out_date')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'room__room_number', 'room__hotel__name')
    date_hierarchy = 'check_in_date'
    readonly_fields = ('total_price', 'amenities_total_price', 'created_at', 'updated_at', 
                      'get_number_of_days', 'get_room_price', 'get_amenities_price')
    fieldsets = (
        (None, {
            'fields': ('user', 'room', 'check_in_date', 'check_out_date', 'number_of_guests')
        }),
        (_('Stay Information'), {
            'fields': ('get_number_of_days', 'get_room_price')
        }),
        (_('Amenities'), {
            'fields': ('selected_amenities', 'get_amenities_price'),
            'description': _('Select amenities for this reservation. Items marked with a price will be charged extra.')
        }),
        (_('Pricing and Status'), {
            'fields': ('total_price', 'status', 'payment_status')
        }),
        (_('Additional Information'), {
            'fields': ('special_requests', 'created_at', 'updated_at')
        })
    )

    def get_number_of_days(self, obj):
        return obj.calculate_number_of_days()
    get_number_of_days.short_description = _('Number of Days')

    def get_room_price(self, obj):
        return f"{obj.calculate_room_price()} MAD"
    get_room_price.short_description = _('Room Total')

    def get_amenities_price(self, obj):
        return f"{obj.calculate_amenities_price()} MAD"
    get_amenities_price.short_description = _('Amenities Total')

    def save_model(self, request, obj, form, change):
        if not change:  # Only for new reservations
            obj.amenities_total_price = obj.calculate_amenities_price()
            obj.total_price = obj.calculate_total_price()
        super().save_model(request, obj, form, change)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('reservation', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('reservation__user__email', 'comment')
