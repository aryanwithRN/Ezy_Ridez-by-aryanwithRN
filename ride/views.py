from django.shortcuts import render
from django.contrib import messages
# Create your views here.

def index(request):
    vehicles = Vehicle.objects.all()
    return render(request, 'index.html', {'vehicles': vehicles})

    # return render(request, 'index.html')

#  Search ride on index page
from datetime import datetime

def index_ride_search(request):
    if request.method == 'POST':
        start = request.POST.get('start')
        destination = request.POST.get('destination')
        date = request.POST.get('date', None)  # Add a default None for date if not provided

        print(f"Received POST request with data: Start - {start}, Destination - {destination}, Date - {date}")

        # Query the database to filter rides based on user input
        if date:
            rides = Ride.objects.filter(
                origin__icontains=start,
                destination__icontains=destination,
                date__gte=date  # Make sure the date is not in the past
            )
        else:
            rides = Ride.objects.filter(
                origin__icontains=start,
                destination__icontains=destination,
                date__gte=datetime.now().date()  # Default to today if no date provided
            )

        return render(request, 'index_ride_search.html', {'rides': rides})

    # Handle GET request (initial load or redirection)
    return render(request, 'index_ride_search.html')

# Rental Vehicle on landing page

def vehicle_list(request):
    vehicles = Vehicle.objects.all()
    return render(request, 'index.html', {'vehicles': vehicles})

from django.shortcuts import render
from .models import Vehicle  # Import your Vehicle model

# def test(request):
#     vehicles = Vehicle.objects.all()  # Query all vehicles from the database
#     return render(request, 'vehicle_section.html', {'vehicles': vehicles})



# for sign up
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

def user_signup(request):
    if request.method == "POST":
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password')
        pass2 = request.POST.get('password1')  # Corrected to match your form field name for password confirmation
        
        if pass1 != pass2:
            error_message = "Passwords do not match"
            return render(request, 'signup.html', {'error_message': error_message})

        # Check if the user already exists
        if User.objects.filter(username=uname).exists():
            error_message = 'Username already exists. Please choose a different username.'
            return render(request, 'signup.html', {'error_message': error_message})

        # Create the user using the User model
        my_user = User.objects.create_user(username=uname, email=email, password=pass1)
        my_user.save()

        # Redirect to the login section on the index page
        return redirect('user_login')  # Adjust the URL if necessary

    return render(request, "signup.html")


# For Login 

from django.contrib.auth import authenticate, login

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username,password)

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Login the user
            login(request, user)
            # Redirect to a success page or dashboard
            return redirect('dashboard')  # Adjust the URL as needed
        else:
            # Authentication failed, show an error message
            error_message = "Invalid username or password."
            return render(request, 'index.html', {'error_message': error_message})

    return render(request, 'login.html')

# logout
from django.contrib.auth import logout
from django.shortcuts import redirect
def user_logout(request):
    logout(request)
    return redirect('index')




# After Login

def dashboard(request):
    return render(request, 'dashboard.html')

# for getting vehicle from database
from .models import Vehicle 
def rent_vehicle(request):
    vehicles = Vehicle.objects.all()
    return render(request, 'rent_vehicle.html', {'vehicles': vehicles})

def post_ride(request):
    return render(request, 'post_ride.html')




# For post ride
from .models import Ride
def post_ride(request):
    if request.method == 'POST':
        # Get user from request
        user = request.user

        # Get form data
        origin = request.POST['origin']
        destination = request.POST['destination']
        date = request.POST['date']
        time = request.POST['time']
        seats_available = request.POST['seats_available']
        price = request.POST['price']
        notes = request.POST['notes']
        car_image = None
        
        if 'car_image' in request.FILES:
            car_image = request.FILES['car_image']

        # Create and save Ride instance
        ride = Ride(
            user=user,
            origin=origin,
            destination=destination,
            date=date,
            time=time,
            seats_available=seats_available,
            price=price,
            notes=notes,
            car_image=car_image
        )
        ride.save()
        return redirect('post_ride')  # Replace 'ride_list' with your success URL

    return render(request, 'post_ride.html')

# see posted ride here
from django.contrib.auth.decorators import login_required

@login_required
def ride_list(request):
    user = request.user
    rides = Ride.objects.filter(user=user) # Assuming Ride is your model for posted rides
    return render(request, 'ride_list.html', {'rides': rides})



# delete posted ride
from django.http import HttpResponse
def delete_ride(request, ride_id):
    if request.method == 'POST':
        try:
            ride_to_delete = Ride.objects.get(pk=ride_id)
            ride_to_delete.delete()
            return redirect('ride_list')  # Redirect to the page where all rides are listed
        except Ride.DoesNotExist:
            return HttpResponse('Ride not found.')  # Display an error message if the ride doesn't exist
    else:
        return HttpResponse('Invalid request method.')  
    

# mark as done
from django.shortcuts import get_object_or_404
def mark_done(request, ride_id):
    ride = get_object_or_404(Ride, pk=ride_id)
    ride.done = True
    ride.save()
    ride.delete()
    return redirect('ride_list')




# search ride {book ride page }
from django.shortcuts import render
from .models import Ride

def book_ride(request):
    if request.method == 'POST':
        start = request.POST.get('start')
        destination = request.POST.get('destination')
        date = request.POST.get('date')

        # Query the database to filter rides based on user input
        rides = Ride.objects.filter(
            origin__icontains=start,
            destination__icontains=destination,
            date=date
        )

        return render(request, 'book_ride.html', {'rides': rides})

    # Handle GET request (initial load or redirection)
    return render(request, 'book_ride.html')




# confirm ride 
from decimal import Decimal  # Import Decimal

@login_required
def booking_confirmation(request, ride_id):
    ride = get_object_or_404(Ride, id=ride_id)
    if request.method == 'POST':
        # Check if there are still seats available
        if ride.seats_available > 0:
            # Store ride details in session
            request.session['ride_id'] = ride_id
            request.session['ride_details'] = {
                'origin': ride.origin,
                'destination': ride.destination,
                'date': str(ride.date),
                'time': str(ride.time),
                'seats_available': ride.seats_available,
                'price': str(ride.price),  # Convert Decimal to string
                'car_image_url': ride.car_image.url
            }
            return render(request, 'booking_confirmation.html', {'ride': ride})
        else:
            return render(request, 'booking_confirmation.html', {'ride': ride, 'error': 'No seats available'})

    return render(request, 'booking_confirmation.html', {'ride': ride})




# confirm booking
@login_required
def confirm_booking(request):
    if request.method == 'POST':
        ride_id = request.session.get('ride_id')
        ride_details = request.session.get('ride_details')

        if not ride_id or not ride_details:
            return redirect('book_ride')  # Redirect to search page if session data is missing

        ride = get_object_or_404(Ride, id=ride_id)

        # Check if there are still seats available
        if ride.seats_available > 0:
            # Create a booking
            Booking.objects.create(
                ride=ride,
                user=request.user,
                email=request.user.email,
                date=ride_details['date'],
                time=ride_details['time'],
                start_from=ride_details['origin'],
                destination=ride_details['destination'],
                booked_car_image=ride.car_image,
                
            )
            # Reduce the available seats by 1
            ride.seats_available -= 1
            ride.save()
            
            # Clear the session data
            del request.session['ride_id']
            del request.session['ride_details']

            # Redirect to a confirmation page or bookings list
            return redirect('booking_page')
        else:
            return render(request, 'booking_confirmation.html', {'ride': ride, 'error': 'No seats available'})

    return redirect('book_ride')

# --------------------------------------------------------------------------------------------------------------------------------

# User Bookings
from .models import Booking

def user_bookings(request):
    bookings = Booking.objects.all()  # Fetch all bookings
    context = {'bookings': bookings}
    return render(request, 'my_bookings.html', context)


def post_vehicle(request):
    if request.method == 'POST':
        vehicle_name = request.POST.get('vehicle_name')
        rent_per_day = request.POST.get('rent_per_day')
        available_count = request.POST.get('available_count')
        vehicle_image = request.FILES.get('vehicle_image')

        # Save the vehicle data to the database
        Vehicle.objects.create(
            owner=request.user,  # Set the owner to the currently logged-in user
            name=vehicle_name,
            rent_price_per_day=rent_per_day,
            available_count=available_count,
            image=vehicle_image
        )
        return redirect('rent_vehicle') 
    
    return render (request, 'post_vehicle.html')



# ---------------------------------------------------------------------------------------------------------------------------------


# rental booking
def rental_booking(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    return render(request, 'rental_booking_page.html', {'vehicle': vehicle})


# rental booking Confirm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import RentalBooking

@csrf_exempt
@login_required
def book_vehicle(request):
    if request.method == 'POST':
        vehicle_name = request.POST.get('vehicle_name')
        vehicle_image = request.POST.get('vehicle_image')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        total_rent = request.POST.get('total_rent')
        user = request.user

        # Convert start_date and end_date to datetime objects
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        # Create and save the booking
        booking = RentalBooking(
            vehicle_name=vehicle_name,
            vehicle_image=vehicle_image,
            start_date=start_date,
            end_date=end_date,
            total_rent=total_rent,
            user=user
        )
        booking.save()

        return JsonResponse({'message': 'Vehicle booked successfully! check Bookings !'})

    return JsonResponse({'error': 'Invalid request'}, status=400)



# ------------------------------------------------------------------------------------------------------------

# My Booking Page 
from .models import Booking, RentalBooking 
def booking_page(request):
    # Fetch ride vehicles and rental vehicles data from the database
    ride_bookings = Booking.objects.all()
    rental_vehicles = RentalBooking.objects.all()

    # Pass the data to the template for rendering
    context = {
        'ride_bookings': ride_bookings,
        'rental_vehicles': rental_vehicles,
    }

    return render(request, 'show_bookings.html', context)


# Ride Cancel Button for ride and renalts
def cancel_ride(request, ride_id):
    if request.method == 'POST':
        ride_booking = get_object_or_404(Booking, id=ride_id)
        ride_booking.delete()
        # Optionally update ride availability count in the actual ride database
        # ride_booking.ride.seats_available += 1
        # ride_booking.ride.save()
    return redirect('booking_page')

def cancel_rental(request, rental_id):
    if request.method == 'POST':
        rental_booking = get_object_or_404(RentalBooking, id=rental_id)
        rental_booking.delete()
        # Optionally update rental availability count in the actual rental database
        # rental_booking.rental_vehicle.available_count += 1
        # rental_booking.rental_vehicle.save()
    return redirect('booking_page')



# Recent Trip Page
from datetime import date
def recent_trips(request):
    # Get today's date
    today = date.today()

    # Query expired bookings
    expired_bookings = RentalBooking.objects.filter(end_date__lt=today)

    # Pass the expired bookings to the template
    context = {
        'expired_bookings': expired_bookings,
    }

    return render(request, 'recent_trip.html', context)

