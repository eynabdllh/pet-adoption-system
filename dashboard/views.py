from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from datetime import datetime, timedelta
from pet_listing.models import Pet
from request_form.models import Adoption
from schedule_form.models import Schedule
from profile_management.models import Profile
from django.http import JsonResponse
from django.db.models import Prefetch

def admin_dashboard(request):
    adopted_count = Pet.objects.filter(is_adopted=True).count()
    available_count = Pet.objects.filter(is_available=True).count()
    total_pet_count = Pet.objects.count()

    # Prefetch the profile via the adopter relationship
    profile_prefetch = Prefetch('adopter', queryset=Profile.objects.select_related('user'))

    pending_requests = Adoption.objects.filter(status="pending").select_related('pet').prefetch_related(profile_prefetch)

    selected_date_str = request.GET.get('date', timezone.now().strftime('%Y-%m-%d'))
    selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()

    calendar_weeks = get_calendar_data(selected_date)
    scheduled_pickups = Schedule.objects.filter(
        day=selected_date.day,
        month=selected_date.strftime('%B'),
        year=selected_date.year,
        completed=False
    )

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
    end_of_month = date.replace(month=date.month % 12 + 1, day=1) - timedelta(days=1)
    current_date = start_of_week

    weeks = []
    while current_date <= end_of_month + timedelta(days=6 - end_of_month.weekday()):
        week = []
        for _ in range(7):
            has_pickup = Schedule.objects.filter(day=current_date.day, month=current_date.strftime('%B'), year=current_date.year, completed=False).exists()
            week.append({
                'date': current_date,
                'is_today': current_date == timezone.now().date(),
                'has_pickup': has_pickup
            })
            current_date += timedelta(days=1)
        weeks.append(week)
    return weeks

def complete_pickup(request, pickup_id):
    if request.method == "POST":
        pickup = get_object_or_404(Schedule, id=pickup_id)
        pickup.completed = True
        pickup.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status=400)
