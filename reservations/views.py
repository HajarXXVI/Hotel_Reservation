from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from django.contrib import messages
from django.db.models import Q
from .models import Room, Reservation, Review, Hotel
from datetime import datetime
from django.core.paginator import Paginator
from .forms import ReviewForm

def home(request):
    hotels = Hotel.objects.all()
    
    # Filtering
    city = request.GET.get('city')
    min_rating = request.GET.get('min_rating')
    amenities = request.GET.getlist('amenities')
    
    if city:
        hotels = hotels.filter(city=city)
    if min_rating:
        hotels = hotels.filter(rating__gte=float(min_rating))
    if amenities:
        for amenity in amenities:
            hotels = hotels.filter(amenities__contains=amenity)
    
    # Sorting
    sort_by = request.GET.get('sort_by', 'name')
    if sort_by == 'rating_desc':
        hotels = hotels.order_by('-rating')
    elif sort_by == 'rating_asc':
        hotels = hotels.order_by('rating')
    elif sort_by == 'name_desc':
        hotels = hotels.order_by('-name')
    else:  # name_asc
        hotels = hotels.order_by('name')
    
    # Get unique cities and amenities for filters
    all_cities = Hotel.MOROCCAN_CITIES
    all_amenities = Hotel.HOTEL_AMENITIES.keys()
    
    context = {
        'hotels': hotels[:6],  # Keep only 6 hotels for featured section
        'all_cities': all_cities,
        'all_amenities': all_amenities,
        'current_filters': {
            'city': city,
            'min_rating': min_rating,
            'amenities': amenities,
            'sort_by': sort_by
        }
    }
    return render(request, 'reservations/home.html', context)

def room_list(request):
    rooms = Room.objects.select_related('hotel').filter(is_available=True)
    
    # Filtering
    hotel_id = request.GET.get('hotel')
    city = request.GET.get('city')
    room_type = request.GET.get('room_type')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    hotel_amenities = request.GET.getlist('hotel_amenities')
    
    if hotel_id:
        try:
            hotel_id = int(hotel_id)
            rooms = rooms.filter(hotel_id=hotel_id)
        except (ValueError, TypeError):
            pass
    
    if city:
        rooms = rooms.filter(hotel__city=city)
    
    if room_type:
        rooms = rooms.filter(room_type=room_type)
    
    if min_price:
        rooms = rooms.filter(price_per_night__gte=float(min_price))
    
    if max_price:
        rooms = rooms.filter(price_per_night__lte=float(max_price))
    
    if hotel_amenities:
        for amenity in hotel_amenities:
            rooms = rooms.filter(hotel__amenities__contains=amenity)
    
    # Sorting
    sort_by = request.GET.get('sort_by', 'price_asc')
    if sort_by == 'price_desc':
        rooms = rooms.order_by('-price_per_night')
    elif sort_by == 'price_asc':
        rooms = rooms.order_by('price_per_night')
    elif sort_by == 'type_desc':
        rooms = rooms.order_by('-room_type')
    elif sort_by == 'type_asc':
        rooms = rooms.order_by('room_type')
    elif sort_by == 'hotel_desc':
        rooms = rooms.order_by('-hotel__name')
    elif sort_by == 'hotel_asc':
        rooms = rooms.order_by('hotel__name')
    
    # Get all hotels, cities, and room types for filters
    all_hotels = Hotel.objects.all()
    all_cities = Hotel.MOROCCAN_CITIES
    all_room_types = Room.ROOM_TYPES
    all_amenities = Hotel.HOTEL_AMENITIES.keys()
    
    context = {
        'rooms': rooms,
        'all_hotels': all_hotels,
        'all_cities': all_cities,
        'all_room_types': all_room_types,
        'all_amenities': all_amenities,
        'current_filters': {
            'hotel_id': hotel_id,
            'city': city,
            'room_type': room_type,
            'min_price': min_price,
            'max_price': max_price,
            'hotel_amenities': hotel_amenities,
            'sort_by': sort_by
        }
    }
    return render(request, 'reservations/room_list.html', context)

def room_detail(request, pk):
    room = get_object_or_404(Room.objects.select_related('hotel'), pk=pk)
    return render(request, 'reservations/room_detail.html', {'room': room})

@login_required
def book_room(request, room_pk):
    room = get_object_or_404(Room, pk=room_pk)
    if request.method == 'POST':
        check_in = datetime.strptime(request.POST['check_in'], '%Y-%m-%d').date()
        check_out = datetime.strptime(request.POST['check_out'], '%Y-%m-%d').date()
        
        # Create the reservation with confirmed status
        reservation = Reservation.objects.create(
            user=request.user,
            room=room,
            check_in_date=check_in,
            check_out_date=check_out,
            number_of_guests=1,  # Default value, you might want to add this to the form
            status='confirmed',  # Changed from 'pending' to 'confirmed'
            payment_status='paid'  # Also set payment status to paid
        )
        
        messages.success(request, _('Room booked successfully! Your reservation is confirmed.'))
        return redirect('reservations:reservation_list')
    
    return render(request, 'reservations/book_room.html', {'room': room})

@login_required
def reservation_list(request):
    reservations = Reservation.objects.filter(user=request.user)
    
    # Status filtering
    status = request.GET.get('status')
    if status:
        reservations = reservations.filter(status=status)
    
    context = {
        'reservations': reservations,
        'current_status': status,
        'all_statuses': [
            ('confirmed', 'Confirmed'),
            ('cancelled', 'Cancelled'),
        ]
    }
    return render(request, 'reservations/reservation_list.html', context)

@login_required
def reservation_detail(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk, user=request.user)
    return render(request, 'reservations/reservation_detail.html', {'reservation': reservation})

@login_required
def cancel_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk, user=request.user)
    if request.method == 'POST':
        reservation.status = 'cancelled'
        reservation.save()
        messages.success(request, _('Reservation cancelled successfully!'))
        return redirect('reservations:reservation_list')
    return render(request, 'reservations/cancel_reservation.html', {'reservation': reservation})

@login_required
def add_review(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk, user=request.user)
    if hasattr(reservation, 'review'):
        messages.info(request, _('You have already reviewed this reservation.'))
        return redirect('reservations:reservation_detail', pk=pk)
    if reservation.status not in ['confirmed', 'completed']:
        messages.warning(request, _('You can only review confirmed or completed reservations.'))
        return redirect('reservations:reservation_detail', pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.reservation = reservation
            review.save()
            messages.success(request, _('Review added successfully!'))
            return redirect('reservations:reservation_detail', pk=pk)
    else:
        form = ReviewForm()
    return render(request, 'reservations/add_review.html', {'reservation': reservation, 'form': form})

def hotel_list(request):
    hotels = Hotel.objects.all().order_by('name')
    paginator = Paginator(hotels, 8)  # 8 hotels per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'reservations/hotel_list.html', {'page_obj': page_obj})
