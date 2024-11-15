from django.shortcuts import render, get_object_or_404, redirect
from .forms import AdoptionForm
from pet_listing.models import Pet
from django.contrib.auth.decorators import login_required
from login_register.decorators import admin_required, adopter_required
from login_register.models import User
from profile_management.models import Profile  
from django.utils import timezone
from .models import Adoption
from django.db.models import Prefetch

@login_required
@adopter_required
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
        # Use only user argument for form instantiation
        form = AdoptionForm(request.POST, user=user)
        if form.is_valid():
            # Save the Adoption instance
            adoption = Adoption.objects.create(
                adopter=user.profile,
                pet=pet,
                first_name=user.first_name,
                last_name=user.last_name,
                age=form.cleaned_data['age'],
                address=form.cleaned_data['address'],
                contact_number=form.cleaned_data['contact_number'],
                email=user.email,
                date=form.cleaned_data['date'],
            )
            # Redirect to the schedule form view with pet_id
            return redirect('schedule', pet_id=pet.id)

    else:
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
    # Fetch query parameters for filtering and sorting
    query = request.GET.get('q', '')
    pet_type = request.GET.get('pet_type', '')
    gender = request.GET.get('gender', '')
    sort_by = request.GET.get('sort_by', 'id')  # Default to 'id' if empty

    # Get all adoption records with related pet and adopter information
    adoptions = Adoption.objects.select_related('pet', 'adopter__user').all()

    # Filter by pet name
    if query:
        adoptions = adoptions.filter(pet__name__icontains=query)
    # Filter by pet type
    if pet_type:
        adoptions = adoptions.filter(pet__pet_type__iexact=pet_type)
    # Filter by gender
    if gender:
        if gender == 'none':
            adoptions = adoptions.filter(pet__gender__isnull=True)
        else:
            adoptions = adoptions.filter(pet__gender__iexact=gender)

    # Order the results
    adoptions = adoptions.order_by(sort_by)

    return render(request, 'adoption_management.html', {
        'adoptions': adoptions,
        'query': query,
        'pet_type': pet_type,
        'gender': gender,
        'sort_by': sort_by,
    })