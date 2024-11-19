import calendar
from django.shortcuts import render, get_object_or_404, redirect
from pet_listing.models import Pet
from .models import Schedule  
from django.contrib.auth.decorators import login_required
from login_register.decorators import adopter_required
from login_register.models import User  
from profile_management.models import Profile
from datetime import datetime
from django.contrib import messages
from request_form.models import Adoption  

@login_required
@adopter_required
def schedule(request, pet_id):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login')

    pet = get_object_or_404(Pet, id=pet_id)
    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(Profile, user=user)

    # Retrieve the adoption form data from the session
    adoption_form_data = request.session.get('adoption_form_data')
    if not adoption_form_data or adoption_form_data.get('pet_id') != pet.id:
        messages.error(request, "Please complete the adoption request form first.")
        return redirect('adopt_form', pet_id=pet.id)

    if request.method == 'POST':
        month = request.POST.get('month')
        day = request.POST.get('day')
        time = request.POST.get('time')
        year = request.POST.get('year')

        if month and day and time and year:
            # Check if the day is valid for the selected month and year
            try:
                month_num = datetime.strptime(month, "%B").month
                num_days = calendar.monthrange(int(year), month_num)[1]  # Get number of days in the month
                if int(day) > num_days:
                    messages.error(request, f"Invalid day for {month} {year}. This month only has {num_days} days.")
                    return redirect('schedule', pet_id=pet.id)
            except ValueError:
                messages.error(request, "Invalid month or year. Please try again.")
                return redirect('schedule', pet_id=pet.id)

            # Create the Schedule record
            Schedule.objects.create(
                pet=pet,
                adopter=user,
                month=month,
                day=int(day),
                year=int(year),
                time=time
            )

            # Finalize the adoption by creating an Adoption instance
            Adoption.objects.create(
                adopter=profile,
                pet=pet,
                first_name=adoption_form_data['first_name'],
                last_name=adoption_form_data['last_name'],
                age=adoption_form_data['age'],
                address=adoption_form_data['address'],
                contact_number=adoption_form_data['contact_number'],
                email=adoption_form_data['email'],
                date=adoption_form_data['date'],
            )

            # Update the pet's status to requested and unavailable
            pet.is_requested = True
            pet.is_available = False
            pet.save()

            # Clear the adoption form data from the session
            del request.session['adoption_form_data']

            messages.success(request, "Pick-up scheduled and adoption finalized successfully!")
            return redirect('my_adoption')
        else:
            messages.error(request, "Please fill in all required fields: month, day, time, and year.")
            
    current_year = datetime.now().year
    years = range(current_year, current_year + 5)  # Include years from current year to next 4 years

    return render(request, 'schedule.html', {
        'pet': pet,
        'user': user,
        'days': range(1, 32),  # You can keep this as-is for now, but you may need to dynamically adjust this
        'morning_hours': [f"{hour}:{minute:02d} AM" for hour in range(9, 12) for minute in (0, 30)],
        'afternoon_hours': [f"{hour}:{minute:02d} PM" for hour in range(1, 6) for minute in (0, 30)],
        'years': years,  # Pass the dynamic years
    })

def pickup_list(request):
    user_id = request.session.get('user_id')
    user = get_object_or_404(User, id=user_id)  
    pickups = Schedule.objects.filter(adopter=user)

    return render(request, 'pickup_list.html', {'pickups': pickups})

def my_adoption(request):
    user_id = request.session.get('user_id')
    user = get_object_or_404(User, id=user_id)  
    pickups = Schedule.objects.filter(adopter=user)

    return render(request, 'my_adoption.html', {'pickups': pickups})

@login_required
def view_details(request, user_id, pet_id):
    user_id = request.session.get('user_id')
    try:
        user = get_object_or_404(User, id=user_id)
        pet = get_object_or_404(Pet, id=pet_id)
        profile = Profile.objects.get(user=user)
        context = {
            'user': user,
            'pet': pet,
            'profile': profile
        }

        return render(request, 'view_details.html', context)
    except Exception as e:
        return render(request, 'my_adoption.html', {'error_message': str(e)})