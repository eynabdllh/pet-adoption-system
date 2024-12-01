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
from notifications.models import Notification

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


    has_notification = Notification.user_has_unread_notifs(user=user)

    Notification.objects.filter(
        user=user,
        title__in=['New Pet Available', 'Pet Status Update'],
        isRead=False
    ).update(isRead=True)

    context = {
        'adopted_pets_count': adopted_pets_count,
        'available_pets_count': available_pets_count,
        'requested_pets_count': requested_pets_count,
        'recently_listed_pets': recently_listed_pets,
        'calendar_weeks': calendar_weeks,
        'pickups': pickups,
        'selected_date': selected_date,
        'has_notification': has_notification,
    }

    return render(request, 'adopter_dashboard.html', context)

@login_required
@admin_required
def admin_dashboard(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    try:
        user = User.objects.get(id=user_id)

        Notification.objects.filter(
            user=user,
            title__in=['New Adoption Request', 'Pickup Schedule Update'],
            isRead=False
        ).update(isRead=True)

        adopted_count = Pet.objects.filter(is_adopted=True).count()
        available_count = Pet.objects.filter(is_available=True).count()
        total_pet_count = Pet.objects.count()

        profile_prefetch = Prefetch('adopter', queryset=Profile.objects.select_related('user'))
        pending_requests = Adoption.objects.filter(
            status="pending",
            pet__is_requested=True
        ).exclude(
            status="cancelled"
        ).select_related('pet').prefetch_related(profile_prefetch)

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

        has_notification = Notification.user_has_unread_notifs(user=request.session.get('user_id'))

        context = {
            'adopted_pets_count': adopted_count,
            'available_pets_count': available_count,
            'total_pets_count': total_pet_count,
            'pending_requests': pending_requests,
            'calendar_weeks': calendar_weeks,
            'pickups': scheduled_pickups,
            'selected_date': selected_date,
            'has_notification': has_notification,
        }

        

        return render(request, 'admin_dashboard.html', context)
    except User.DoesNotExist:
        messages.error(request, "User not found")
        return redirect('login')

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
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    try:
        user = User.objects.get(id=user_id)
        pet = get_object_or_404(Pet, id=pet_id)
        
        Notification.objects.filter(
            user=user,
            pet=pet,
            isRead=False
        ).update(isRead=True)

        has_notification = Notification.user_has_unread_notifs(user=request.session.get('user_id'))

        request.session['prev_url'] = request.META.get('HTTP_REFERER', '/')
        return render(request, 'view_pet.html', {'pet': pet,'has_notification': has_notification})
    except User.DoesNotExist:
        return redirect('login')

@login_required
@admin_required
def review_form_detail(request, pet_id):
    adoption = get_object_or_404(Adoption.objects.select_related('adopter__user'), pet__id=pet_id)
    profile = adoption.adopter
    pet = adoption.pet

    if request.method == 'POST':
        status = request.POST.get('status')
        reason = request.POST.get('reason')

        try:
            if status == 'approved':
                if not pet.is_approved:
                    pet.is_requested = False
                    pet.is_approved = True
                    pet.is_upcoming = True
                    pet.save()

                    adoption.status = 'approved'
                    adoption.save()

                    messages.success(request, f"Pet {pet.name} has been approved for adoption.")

                    Notification.objects.create_for_adopter(
                        adopter=profile.user,
                        title="Adoption Request Approved",
                        message=f"Your adoption request for {pet.name} has been approved! Please check your schedule for pickup details.",
                        pet=pet
                    )

            elif status == 'rejected':
                if reason:
                    if not pet.is_rejected:
                        pet.is_requested = False
                        pet.is_rejected = True
                        pet.is_adopted = False
                        pet.save()

                        adoption.status = 'rejected'
                        adoption.reason_choices = reason
                        adoption.save()

                        messages.success(request, "The pet adoption request has been rejected.")

                        Notification.objects.create_for_adopter(
                            adopter=profile.user,
                            title="Adoption Request Rejected",
                            message=f"Your adoption request for {pet.name} has been rejected. Reason: {reason}",
                            pet=pet
                        )

        except Exception as e:
            messages.error(request, f"An error occurred: {e}")

    return render(request, 'review_form.html', {'adoption': adoption, 'profile': profile})