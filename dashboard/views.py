from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from datetime import datetime, timedelta
from pet_listing.models import Pet
from request_form.models import Adoption
from schedule_form.models import Schedule
from django.http import JsonResponse

def admin_dashboard(request):
    adopted_count = Pet.objects.filter(is_adopted=True).count()
    available_count = Pet.objects.filter(is_available=True).count()
    total_pet_count = Pet.objects.count()

    pending_requests = Adoption.objects.filter(status="Pending")

    today = timezone.now().date()
    selected_date = request.GET.get('date')

    if selected_date:
        selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
    else:
        selected_date = today

    calendar_weeks = get_calendar_data(selected_date)

    scheduled_pickups = Schedule.objects.filter(scheduled_at__date=selected_date)
    #scheduled_pickups = Schedule.objects.filter(scheduled_at__date=selected_date, completed=False)

    context = {
        'adopted_pets_count': adopted_count,
        'available_pets_count': available_count,
        'total_pets_count': total_pet_count,
        'adoption_requests': pending_requests,
        'calendar_weeks': calendar_weeks,
        'pickups': scheduled_pickups,
        'selected_date': selected_date,
    }

    return render(request, 'admin_dashboard.html', context)

def get_calendar_data(date):
    start_of_month = date.replace(day=1)
    start_of_week = start_of_month - timedelta(days=start_of_month.weekday())
    days_in_month = (date.replace(month=date.month % 12 + 1, day=1) - timedelta(days=1)).day

    weeks = []
    current_date = start_of_week
    for _ in range(6): 
        week = []
        for _ in range(7): 
            week.append({
                'date': current_date,
                'has_pickup': Schedule.objects.filter(scheduled_at__date=current_date).exists(),
            })
            current_date += timedelta(days=1)
        weeks.append(week)
        if current_date.day == 1 and current_date.month != start_of_month.month:
            break
    return weeks

def complete_pickup(request, pickup_id):
    if request.method == "POST":
        pickup = get_object_or_404(Schedule, id=pickup_id)
        #pickup.completed = True
        pickup.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status=400)
