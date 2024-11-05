from django.shortcuts import render, get_object_or_404, redirect
from pet_listing.models import Pet
from .models import Schedule  
from django.contrib.auth.decorators import login_required
from login_register.models import User  
from datetime import datetime
from django.contrib import messages
from request_form.models import Adoption  

@login_required
def schedule(request, pet_id):
    user_id = request.session.get('user_id')  
    if not user_id:
        return redirect('login')  

    pet = get_object_or_404(Pet, id=pet_id)
    user = get_object_or_404(User, id=user_id) 

    if request.method == 'POST':
        print("Received POST data:", request.POST)  
        month = request.POST.get('month')
        day = request.POST.get('day')
        time = request.POST.get('time')
        year = request.POST.get('year')

        if month and day and time and year:

            latest_adoption_form = Adoption.objects.filter(adopter=user, pet=pet).last()

            if latest_adoption_form:
                Schedule.objects.create(
                    pet=pet,
                    adopter=user,  
                    month=month,
                    day=int(day),
                    year=int(year),
                    time=time
                )
                messages.success(request, "Pick-up scheduled successfully!")
                return redirect('success') 
            else:
                messages.error(request, "No adoption form found for the user and pet.")
        else:
            messages.error(request, "Please fill in all required fields: month, day, time, and year.")

    days = range(1, 32) 
    morning_hours = [f"{hour}:{minute:02d} AM" for hour in range(9, 12) for minute in (0, 30)]
    afternoon_hours = [f"{hour}:{minute:02d} PM" for hour in range(1, 6) for minute in (0, 30)]
    years = [datetime.now().year]

    return render(request, 'schedule.html', {
        'pet': pet,
        'user': user,  
        'days': days,
        'morning_hours': morning_hours,
        'afternoon_hours': afternoon_hours,
        'years': years
    })

def success(request):
    return render(request, 'success.html')  # Render a success template or redirect as necessary


def pickup_list(request):
    user_id = request.session.get('user_id')
    user = get_object_or_404(User, id=user_id)
    pickups = Schedule.objects.filter(adopter=user)
    
    return render(request, 'pickup_list.html', {'pickups': pickups})