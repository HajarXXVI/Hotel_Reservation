from django.urls import path
from . import views

app_name = 'reservations'

urlpatterns = [
    path('', views.home, name='home'),
    path('rooms/', views.room_list, name='room_list'),
    path('rooms/<int:pk>/', views.room_detail, name='room_detail'),
    path('book/<int:room_pk>/', views.book_room, name='book_room'),
    path('reservations/', views.reservation_list, name='reservation_list'),
    path('reservations/<int:pk>/', views.reservation_detail, name='reservation_detail'),
    path('reservations/<int:pk>/cancel/', views.cancel_reservation, name='cancel_reservation'),
    path('reservations/<int:pk>/review/', views.add_review, name='add_review'),
    path('hotels/', views.hotel_list, name='hotel_list'),
] 