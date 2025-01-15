# ride/admin.py

from django.contrib import admin
from .models import Vehicle,Ride,Booking
# Ride, Car

admin.site.register(Vehicle)
admin.site.register(Ride)
admin.site.register(Booking)
