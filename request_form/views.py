from django.shortcuts import render, get_object_or_404, redirect
from .forms import AdoptionForm
from pet_listing.models import Pet
from django.contrib.auth.decorators import login_required
from login_register.models import User
from django.utils import timezone
from .models import Adoption 

@login_required 
def adopt_form(request, pet_id):
    user_id = request.session.get('user_id') 
    pet = get_object_or_404(Pet, id=pet_id)

    if not user_id:
        return redirect('login')  

    user = User.objects.get(id=user_id)  

    if request.method == 'POST':
        form = AdoptionForm(request.POST)
        if form.is_valid():
            # Temporarily save the data in the session
            request.session['adoption_data'] = {
                'adopter_id': user_id,
                'pet_id': pet_id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'age': form.cleaned_data['age'],
                'contact_number': form.cleaned_data['contact_number'],
                'address': form.cleaned_data['address'],
                'email': user.email,
                'date': form.cleaned_data['date'].strftime('%Y-%m-%d'),  
            }
            return redirect('confirmation')  
        else:
            print(form.errors) 
    else:
        form = AdoptionForm() 

    today = timezone.localdate()  
    return render(request, 'adopt_form.html', {
        'form': form,
        'pet': pet,
        'today': today.isoformat(),
        'user': user  
    })

def confirmation(request):
    adoption_data = request.session.get('adoption_data')
    
    if not adoption_data:
        return redirect('adopt_form')  

    pet = get_object_or_404(Pet, id=adoption_data['pet_id'])
    user = User.objects.get(id=adoption_data['adopter_id'])

    if request.method == 'POST': 
        # Check if there's already an adoption record
        adoption, created = Adoption.objects.get_or_create(
            adopter=user,
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

        if not created:  # If the adoption already exists, update its details
            adoption.first_name = adoption_data['first_name']
            adoption.last_name = adoption_data['last_name']
            adoption.age = adoption_data['age']
            adoption.contact_number = adoption_data['contact_number']
            adoption.address = adoption_data['address']
            adoption.email = adoption_data['email']
            adoption.date = adoption_data['date']
            adoption.save()  

        del request.session['adoption_data'] 
        return redirect('schedule', pet_id=pet.id)  

    return render(request, 'confirmation.html', {
        'adoption_data': adoption_data,
        'pet': pet,
        'user': user,
    })
