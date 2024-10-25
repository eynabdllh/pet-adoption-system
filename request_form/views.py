#views.py request_form app
from django.shortcuts import render, get_object_or_404, redirect
from .forms import AdoptionForm
from pet_listing.models import Pet
from django.contrib.auth.decorators import login_required
from login_register.models import User
from django.utils import timezone
from .models import Adoption  # Ensure to import your Adoption model

@login_required 
def adopt_form(request, pet_id):
    user_id = request.session.get('user_id')  # Get the logged-in user ID from the session
    pet = get_object_or_404(Pet, id=pet_id)

    if not user_id:
        return redirect('login')  # If user is not logged in, redirect to login page

    user = User.objects.get(id=user_id)  # Fetch the logged-in user

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
                'date': form.cleaned_data['date'].strftime('%Y-%m-%d'),  # Convert date to string
            }
            return redirect('confirmation')  # Redirect to confirmation page
        else:
            print(form.errors)  # Log form errors for debugging
    else:
        form = AdoptionForm()  # Create an empty form instance

    today = timezone.localdate()   # Get today's date
    return render(request, 'adopt_form.html', {
        'form': form,
        'pet': pet,
        'today': today.isoformat(),
        'user': user  # Pass the user object to the template
    })

def confirmation(request):
    adoption_data = request.session.get('adoption_data')
    
    if not adoption_data:
        return redirect('adopt_form')  # Redirect back if there's no data

    pet = get_object_or_404(Pet, id=adoption_data['pet_id'])
    user = User.objects.get(id=adoption_data['adopter_id'])

    if request.method == 'POST':  # User clicked "Confirm" on the confirmation page
        # Create and save the adoption object
        adoption = Adoption.objects.create(
            adopter=user,
            pet=pet,
            first_name=adoption_data['first_name'],
            last_name=adoption_data['last_name'],
            age=adoption_data['age'],
            contact_number=adoption_data['contact_number'],
            address=adoption_data['address'],
            email=adoption_data['email'],
            date=adoption_data['date'],
        )
        del request.session['adoption_data']  # Clear session data
        return redirect('schedule', pet_id=pet.id)  # Redirect to a success page

    # If GET request, render the confirmation page
    return render(request, 'confirmation.html', {
        'adoption_data': adoption_data,
        'pet': pet,
        'user': user,
    })
