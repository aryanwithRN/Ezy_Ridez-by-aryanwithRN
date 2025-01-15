from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index,name='index'),

    
    path('signup/',views.user_signup,name='signup'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='logout'),

    # Landing page
    path('vehicles/', views.vehicle_list, name='vehicle_list'),

    # DASHBOARD
    path('dashboard', views.dashboard, name='dashboard'),

    # Features
    path('book_ride', views.book_ride, name='book_ride'),
   
    # confrim booking
    path('booking-confirmation/<int:ride_id>/', views.booking_confirmation, name='booking_confirmation'),
    path('confirm-booking/', views.confirm_booking, name='confirm_booking'),
    # user booking
    path('user_bookings/', views.user_bookings, name='user_bookings'),
    
    # Rent Vehicle    
    path('rent_vehicle', views.rent_vehicle, name='rent_vehicle'), 

    # post ride
    path('post_ride/', views.post_ride, name='post_ride'),
    path('rides/', views.ride_list, name='ride_list'), 

    # delete post ride
    path('delete_ride/<int:ride_id>/', views.delete_ride, name='delete_ride'),

    # mark as done post ride
    path('mark_done/<int:ride_id>/', views.mark_done, name='mark_done'),

    # Search ride on index page
    path('index_ride_search', views.index_ride_search, name='index_ride_search'),

    # Post Vehicle
    path('post_vehicle',views.post_vehicle,name='post_vehicle'),   

    #  Rental Booking
    path('rent/<int:vehicle_id>/', views.rental_booking, name='rental_booking_page'),

    #  Store Rental Detials 
    path('book_vehicle/', views.book_vehicle, name='book_vehicle'),

    # show my booking toggle
    path('booking_page/', views.booking_page, name='booking_page'),

    # Cancel ride 
    path('cancel-ride/<int:ride_id>/', views.cancel_ride, name='cancel_ride'),

    # Cancel rental
    path('cancel-rental/<int:rental_id>/', views.cancel_rental, name='cancel_rental'),
    # Recent Trips
    path('recent-trips/', views.recent_trips, name='recent_trips'),

    # test
    # path('vehicle_section', views.test, name='test')    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)