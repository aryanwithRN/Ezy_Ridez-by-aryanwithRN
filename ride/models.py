from django.db import models
from django.contrib.auth.models import User 
# For rent vehicle
class Vehicle(models.Model):
    owner = models.CharField(max_length=100, default='')
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='vehicle_images/')
    rent_price_per_day = models.DecimalField(max_digits=8, decimal_places=2)
    available_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name



# For Post Ride

class Ride(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ForeignKey to link with User
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    seats_available = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    notes = models.TextField(blank=True, null=True)
    car_image = models.ImageField(upload_to='car_images/', blank=True, null=True)

    def __str__(self):
        return f"Ride from {self.origin} to {self.destination} on {self.date} at {self.time}"
    


# To Book

from django.urls import reverse
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE)
    email = models.EmailField()
    date = models.DateField()
    time = models.TimeField()
    start_from = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    booked_car_image = models.ImageField(upload_to='booking_images/', null=True, blank=True)

    def __str__(self):
        return f"Booking by {self.user.email} for {self.ride.car_name} on {self.date}"

    def get_absolute_url(self):
        return reverse('booking_detail', kwargs={'pk': self.pk})


class RentalBooking(models.Model):
    vehicle_name = models.CharField(max_length=255)
    vehicle_image = models.ImageField(upload_to='vehicle_images/')
    total_rent = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    start_date = models.DateField()
    end_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.vehicle_name} - {self.user.username}'s Booking"