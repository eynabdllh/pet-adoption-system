from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from datetime import datetime
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

    scheduled_pickups = Schedule.objects.filter(scheduled_at__date=selected_date)

    context = {
        'adopted_count': adopted_count,
        'available_count': available_count,
        'total_pet_count': total_pet_count,
        'pending_requests': pending_requests,
        'scheduled_pickups': scheduled_pickups,
        'selected_date': selected_date,
        'today': today,
    }

    return render(request, 'admin_dashboard.html', context)

def complete_pickup(request, pickup_id):
    if request.method == "POST":
        pickup = get_object_or_404(Schedule, id=pickup_id)
        pickup.completed = True
        pickup.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status=400)