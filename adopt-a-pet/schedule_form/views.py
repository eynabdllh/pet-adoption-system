import calendar
import json
from django.http import JsonResponse
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
from django.views.decorators.csrf import csrf_exempt
from notifications.models import Notification

@login_required
@adopter_required
def schedule(request, pet_id):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login')

    pet = get_object_or_404(Pet, id=pet_id)
    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(Profile, user=user)

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
            try:
                month_num = datetime.strptime(month, "%B").month
                num_days = calendar.monthrange(int(year), month_num)[1] 
                if int(day) > num_days:
                    messages.error(request, f"Invalid day for {month} {year}. This month only has {num_days} days.")
                    return redirect('schedule', pet_id=pet.id)
            except ValueError:
                messages.error(request, "Invalid month or year. Please try again.")
                return redirect('schedule', pet_id=pet.id)

            Schedule.objects.create(
                pet=pet,
                adopter=user,
                month=month,
                day=int(day),
                year=int(year),
                time=time
            )

            pet.is_requested = True
            pet.is_available = False
            pet.save()

            del request.session['adoption_form_data']

            messages.success(request, "Pick-up scheduled successfully!")
            return redirect('my_adoption')
        else:
            messages.error(request, "Please fill in all required fields: month, day, time, and year.")
            
    current_year = datetime.now().year
    years = range(current_year, current_year + 5) 

    has_notification = Notification.user_has_unread_notifs(user=request.session.get('user_id'))

    return render(request, 'schedule.html', {
        'pet': pet,
        'user': user,
        'days': range(1, 32), 
        'morning_hours': [f"{hour}:{minute:02d} AM" for hour in range(9, 12) for minute in (0, 30)],
        'afternoon_hours': [f"{hour}:{minute:02d} PM" for hour in range(1, 6) for minute in (0, 30)],
        'years': years,
        'has_notification': has_notification,
    })

@login_required
@adopter_required
def pickup_list(request):
    user_id = request.session.get('user_id')
    user = get_object_or_404(User, id=user_id) 
    pickups = Schedule.objects.filter(adopter=user)

    has_notification = Notification.user_has_unread_notifs(user=request.session.get('user_id'))

    return render(request, 'pickup_list.html', {'pickups': pickups, 'has_notification': has_notification})


@csrf_exempt  
@login_required
def my_adoption(request):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "User not logged in.")
        return redirect('my_adoption')  # Redirect to the same page or another page

    try:
        user = get_object_or_404(User, id=user_id)
    except Exception as e:
        messages.error(request, f"Invalid user: {e}")
        return redirect('my_adoption')

    try:
        pickups = Schedule.objects.filter(adopter=user).select_related('pet')
    except Exception as e:
        messages.error(request, f"Query error: {e}")
        return redirect('my_adoption')

    certificate_data = []
    for pickup in pickups:
        if pickup.pet.is_adopted:  
            certificate_data.append({
                'adopter_name': f"{user.first_name} {user.last_name}",
                'pet_name': pickup.pet.name,
                'adoption_date': f"{pickup.month} {pickup.day}, {pickup.year}",
            })

    if request.method == 'POST':
        pet_id = request.POST.get('pet_id')  # Get form data
        reason = request.POST.get('reason')

        if not pet_id:
            messages.error(request, "Pet ID is missing.")
            return redirect('my_adoption')
        if not reason:
            messages.error(request, "Cancellation reason is missing.")
            return redirect('my_adoption')

        try:
            pet = get_object_or_404(Pet, id=pet_id)
            schedule = get_object_or_404(Schedule, pet=pet, adopter=user)

            pet.is_requested = False
            pet.is_cancelled = True
            pet.save()

            schedule.cancelled = True
            schedule.reason_choices = reason
            schedule.save()

            messages.success(request, f"Pet {pet.name} is now cancelled.")
            return redirect('my_adoption')
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return redirect('my_adoption')
    
    has_notification = Notification.user_has_unread_notifs(user=request.session.get('user_id'))

    return render(request, 'my_adoption.html', {
        'pickups': pickups,
        'certificate_data': certificate_data,
        'has_notification': has_notification,
    })


@login_required
@adopter_required
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