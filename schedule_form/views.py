# views.py in schedule_form app
from django.shortcuts import render, get_object_or_404, redirect
from pet_listing.models import Pet
from .models import Schedule  # Import your Schedule model
from django.contrib.auth.decorators import login_required
from login_register.models import User  # Use the same User model as in request_form
from datetime import datetime
from django.contrib import messages
from request_form.models import Adoption  # Import the Adoption model to check if the user has adopted

@login_required
def schedule(request, pet_id):
    user_id = request.session.get('user_id')  # Fetch user_id from session for consistency
    if not user_id:
        return redirect('login')  # Redirect to login if no user_id in session

    pet = get_object_or_404(Pet, id=pet_id)
    user = get_object_or_404(User, id=user_id)  # Fetch the logged-in user based on user_id from session

    if request.method == 'POST':
        print("Received POST data:", request.POST)  # Debugging line
        month = request.POST.get('month')
        day = request.POST.get('day')
        time = request.POST.get('time')
        year = request.POST.get('year')

        # Ensure all required fields are filled
        if month and day and time and year:

            # Verify if the user has an adoption record for the pet
            latest_adoption_form = Adoption.objects.filter(adopter=user, pet=pet).last()

            if latest_adoption_form:
                # Create a Schedule instance for the pick-up
                Schedule.objects.create(
                    pet=pet,
                    adopter=user,  # Directly use the User instance
                    month=month,
                    day=int(day),
                    year=int(year),
                    time=time
                )
                messages.success(request, "Pick-up scheduled successfully!")
                return redirect('success')  # Redirect to a success page
            else:
                messages.error(request, "No adoption form found for the user and pet.")
        else:
            messages.error(request, "Please fill in all required fields: month, day, time, and year.")

    # Prepare data for rendering the schedule form
    days = range(1, 32)  # Adjust for specific months if necessary
    morning_hours = [f"{hour}:{minute:02d} AM" for hour in range(9, 12) for minute in (0, 30)]
    afternoon_hours = [f"{hour}:{minute:02d} PM" for hour in range(1, 6) for minute in (0, 30)]
    years = [datetime.now().year]

    return render(request, 'schedule.html', {
        'pet': pet,
        'user': user,  # Pass user to the template for consistency
        'days': days,
        'morning_hours': morning_hours,
        'afternoon_hours': afternoon_hours,
        'years': years
    })

def success(request):
    return render(request, 'success.html')  # Render a success template or redirect as necessary
