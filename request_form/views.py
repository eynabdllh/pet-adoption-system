import json
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .forms import AdoptionForm
from pet_listing.models import Pet
from schedule_form.models import Schedule
from django.contrib.auth.decorators import login_required
from login_register.decorators import admin_required, adopter_required
from login_register.models import User
from profile_management.models import Profile  
from django.utils import timezone
from .models import Adoption

@login_required
def adopt_form(request, pet_id):
    user_id = request.session.get('user_id')
    pet = get_object_or_404(Pet, id=pet_id)

    if not user_id:
        return redirect('login')

    user = User.objects.get(id=user_id)
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        # Use posted data to initialize the form
        form = AdoptionForm(request.POST, user=user)
        if form.is_valid():
            # Save the adoption data
            adoption = Adoption.objects.create(
                adopter=user.profile if hasattr(user, 'profile') else None,  # Profile might not exist
                pet=pet,
                first_name=form.cleaned_data.get('first_name', user.first_name),
                last_name=form.cleaned_data.get('last_name', user.last_name),
                age=form.cleaned_data['age'],
                address=form.cleaned_data['address'],
                contact_number=form.cleaned_data['contact_number'],
                email=form.cleaned_data.get('email', user.email),
                date=form.cleaned_data['date'],
            )
            
            pet.is_requested = True
            pet.is_available = False
            pet.save()

            # Store adoption data in session for later use
            request.session['adoption_form_data'] = {
                'adopter_id': user.profile.id if profile else user.id,
                'pet_id': pet.id,
                'first_name': adoption.first_name,
                'last_name': adoption.last_name,
                'age': adoption.age,
                'address': adoption.address,
                'contact_number': adoption.contact_number,
                'email': adoption.email,
                'date': adoption.date.isoformat(),
            }

            return redirect('schedule', pet_id=pet.id)
    else:
        # Initialize form data with user details if available
        initial_data = {
            'adopter_id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
        }

        if profile:
            initial_data.update({
                'age': profile.age if profile.age else '',
                'address': profile.address if profile.address else '',
                'contact_number': profile.phone_number if profile.phone_number else '',
            })

        form = AdoptionForm(initial=initial_data, user=user)

    today = timezone.localdate()
    return render(request, 'adopt_form.html', {
        'form': form,
        'pet': pet,
        'today': today.isoformat(),
        'user': user,
    })

@login_required
@admin_required
def adoption_management(request):
    status = request.GET.get('status', 'requested')  

    if status == 'adopted':
        pets = Pet.objects.filter(is_adopted=True).prefetch_related('adoption_set')
    elif status == 'rejected':
        pets = Pet.objects.filter(is_rejected=True).prefetch_related('adoption_set')
    else: 
        pets = Pet.objects.filter(is_requested=True).prefetch_related('adoption_set')
        
    adoptions = Adoption.objects.all()
    return render(request, 'adoption_management.html', {
        'pets': pets,
        'status': status, 
        'adoptions': adoptions,
    })

@login_required
@admin_required
def review_form(request, pet_id):
    adoption = get_object_or_404(Adoption.objects.select_related('adopter__user'), pet__id=pet_id)
    profile = adoption.adopter

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            status = data.get('status')
            reason = data.get('reason')  

            pet = adoption.pet

            if status == 'adopted':
                pet.is_requested = False
                pet.is_adopted = True
                pet.save()

                adoption.status = 'approved'
                adoption.reason_choices = None  
                adoption.save()

                return JsonResponse({'success': True, 'message': 'The pet has been marked as adopted.'})

            elif status == 'rejected':
                if not reason:
                    return JsonResponse({'success': False, 'message': 'A reason is required for rejection.'})

                pet.is_requested = False
                pet.is_rejected = True
                pet.save()

                adoption.status = 'rejected'
                adoption.reason_choices = reason  # Save the rejection reason
                adoption.save()
                messages.success(request, 'Pet is now rejected')
                return redirect('/adoption_management/?status=adopted')

            else:
                return JsonResponse({'success': False, 'message': 'Invalid status provided.'})

        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error: {str(e)}'})

    return render(request, 'review_form.html', {
        'adoption': adoption,
        'profile': profile
    })

@login_required
@admin_required
def admin_pickup(request):
    status = request.GET.get('status', 'upcoming')  # Default to 'requested'

    if status == 'completed':
        schedules = Schedule.objects.filter(completed=True).prefetch_related('adoption_set')
    elif status == 'cancelled':
        schedules = Schedule.objects.filter(cancelled=True).prefetch_related('adoption_set')
    else:  
        schedules = Schedule.objects.filter(upcoming=True).prefetch_related('adoption_set')

    return render(request, 'admin_pickup.html', {
        'schedules': schedules,
        'status': status,  
    })