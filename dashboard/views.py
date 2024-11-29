import json
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from login_register.decorators import admin_required, adopter_required
from django.utils import timezone
from datetime import datetime, timedelta
from pet_listing.models import Pet
from request_form.models import Adoption
from schedule_form.models import Schedule
from profile_management.models import Profile
from login_register.models import User
from django.db.models import Prefetch

@login_required
@adopter_required
def adopter_dashboard(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login')

    user = User.objects.get(id=user_id)
    profile, created = Profile.objects.get_or_create(user=user)
    adopted_pets_count = Pet.objects.filter(is_adopted=True, adoption__adopter=profile).count()
    available_pets_count = Pet.objects.filter(is_available=True).count()
    requested_pets_count = Pet.objects.filter(is_requested=True, adoption__adopter=profile).count()

    recently_listed_pets = Pet.objects.filter(is_available=True).order_by('-id')

    selected_date_str = request.GET.get('date', timezone.now().strftime('%Y-%m-%d'))
    selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()

    calendar_weeks = get_calendar_data(selected_date)
    pickups = Schedule.objects.filter(
        day=selected_date.day, 
        month=selected_date.strftime('%B'), 
        year=selected_date.year,  
        pet__is_upcoming=True,  
        pet__is_approved = True, 
        pet__is_adopted=False, 
        adopter=user
    )

    context = {
        'adopted_pets_count': adopted_pets_count,
        'available_pets_count': available_pets_count,
        'requested_pets_count': requested_pets_count,
        'recently_listed_pets': recently_listed_pets,
        'calendar_weeks': calendar_weeks,
        'pickups': pickups,
        'selected_date': selected_date,
    }

    return render(request, 'adopter_dashboard.html', context)

@login_required
@admin_required
def admin_dashboard(request):

    adopted_count = Pet.objects.filter(is_adopted=True).count()
    available_count = Pet.objects.filter(is_available=True).count()
    total_pet_count = Pet.objects.count()

    profile_prefetch = Prefetch('adopter', queryset=Profile.objects.select_related('user'))
    pending_requests = Adoption.objects.filter(status="pending").select_related('pet').prefetch_related(profile_prefetch)

    selected_date_str = request.GET.get('date', timezone.now().strftime('%Y-%m-%d'))
    selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()

    calendar_weeks = get_calendar_data(selected_date)

    scheduled_pickups = Schedule.objects.filter(
        day=selected_date.day,
        month=selected_date.strftime('%B'),
        year=selected_date.year,
        pet__is_upcoming=True,  
        pet__is_approved = True,
        pet__is_adopted=False 
    ).select_related('pet', 'adopter')

    context = {
        'adopted_pets_count': adopted_count,
        'available_pets_count': available_count,
        'total_pets_count': total_pet_count,
        'pending_requests': pending_requests,
        'calendar_weeks': calendar_weeks,
        'pickups': scheduled_pickups,
        'selected_date': selected_date,
    }

    return render(request, 'admin_dashboard.html', context)

def get_calendar_data(date):
    start_of_month = date.replace(day=1) 
    start_of_week = start_of_month - timedelta(days=start_of_month.weekday())
    if date.month == 12:
        end_of_month = date.replace(day=31)
    else:
        end_of_month = date.replace(month=date.month + 1, day=1) - timedelta(days=1)  
    
    current_date = start_of_week 

    weeks = []
    while current_date <= end_of_month + timedelta(days=6 - end_of_month.weekday()):
        week = []
        for _ in range(7):
            has_pickup = Schedule.objects.filter(day=current_date.day, month=current_date.strftime('%B'), year=current_date.year, pet__is_upcoming=True, pet__is_approved = True).exists()
            week.append({
                'date': current_date,
                'is_today': current_date == timezone.now().date(),
                'has_pickup': has_pickup
            })
            current_date += timedelta(days=1)
        weeks.append(week)
    return weeks

@login_required
@adopter_required
def view_pet_detail(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)

    request.session['prev_url'] = request.META.get('HTTP_REFERER', '/')
    return render(request, 'view_pet.html', {'pet': pet})

@login_required
@admin_required
def review_form_detail(request, pet_id):
    adoption = get_object_or_404(Adoption.objects.select_related('adopter__user'), pet__id=pet_id)
    profile = adoption.adopter

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            status = data.get('status')
            reason = data.get('reason')

            if status not in ['approved', 'rejected']:
                messages.error(request, 'Invalid status provided.')
                return JsonResponse({'success': False, 'message': 'Invalid status provided.'})

            pet = adoption.pet

            if status == 'approved':
                pet.is_requested = False
                pet.is_approved = True
                pet.is_upcoming = True
                pet.save()

                adoption.status = 'approved'
                adoption.save()

                messages.success(request, f"Pet {pet.name} has been approved for adoption.")
                return JsonResponse({'success': True, 'message': f"Pet {pet.name} has been approved for adoption."})

            elif status == 'rejected':
    
                if not reason:
                    messages.error(request, "A reason is required for rejection.")
                    return JsonResponse({'success': False, 'message': "A reason is required for rejection."})

                pet.is_requested = False
                pet.is_rejected = True
                pet.is_adopted = False
                pet.save()

                adoption.status = 'rejected'
                adoption.reason_choices = reason
                adoption.save()

                messages.success(request, "The pet adoption request has been rejected.")
                return JsonResponse({'success': True, 'message': "The pet adoption request has been rejected."})

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON format.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f"An error occurred: {str(e)}"})

    return render(request, 'review_form.html', {'adoption': adoption, 'profile': profile}) 