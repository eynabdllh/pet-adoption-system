from django.shortcuts import render, get_object_or_404, redirect
from .forms import AdoptionForm
from pet_listing.models import Pet
from django.contrib.auth.decorators import login_required
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

    # Attempt to retrieve the user's Profile data
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        # Pass only `user` as the keyword argument to avoid the TypeError
        form = AdoptionForm(request.POST, user=user)
        if form.is_valid():
            request.session['adoption_data'] = {
                'adopter_id': user_id,
                'pet_id': pet_id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'age': form.cleaned_data['age'],
                'address': form.cleaned_data['address'],
                'contact_number': form.cleaned_data['contact_number'],
                'email': user.email,
                'date': form.cleaned_data['date'].strftime('%Y-%m-%d'),
            }
            return redirect('confirmation')
    else:
        # Pass initial data explicitly
        initial_data = {
            'adopter_id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
        }

        if profile:
            initial_data.update({
                'age': profile.age,
                'address': profile.address,
                'contact_number': profile.phone_number,
            })

        # Pass only `user` as a keyword argument
        form = AdoptionForm(initial=initial_data, user=user)

    today = timezone.localdate()
    return render(request, 'adopt_form.html', {
        'form': form,
        'pet': pet,
        'today': today.isoformat(),
        'user': user,
    })

def confirmation(request):
    adoption_data = request.session.get('adoption_data')
    
    if not adoption_data:
        return redirect('adopt_form')  

    pet = get_object_or_404(Pet, id=adoption_data['pet_id'])

    # Get or create the Profile instance based on the adopter_id (user ID)
    user = get_object_or_404(User, id=adoption_data['adopter_id'])
    profile = Profile.objects.get(user=user)

    if request.method == 'POST': 
        adoption, created = Adoption.objects.get_or_create(
            adopter=profile,  # Make sure to use the profile instance here
            pet=pet,
            defaults={
                'first_name': adoption_data['first_name'],
                'last_name': adoption_data['last_name'],
                'age': adoption_data['age'],
                'contact_number': adoption_data['contact_number'],
                'address': adoption_data['address'],
                'email': adoption_data['email'],
                'date': adoption_data['date'],
            }
        )

        if not created:  # If adoption record exists, update the record
            adoption.first_name = adoption_data['first_name']
            adoption.last_name = adoption_data['last_name']
            adoption.age = adoption_data['age']
            adoption.contact_number = adoption_data['contact_number']
            adoption.address = adoption_data['address']
            adoption.email = adoption_data['email']
            adoption.date = adoption_data['date']
            adoption.save()  

        # Clear session data after successful save
        del request.session['adoption_data'] 
        return redirect('schedule', pet_id=pet.id)  

    return render(request, 'confirmation.html', {
        'adoption_data': adoption_data,
        'pet': pet,
        'user': user,
    })
