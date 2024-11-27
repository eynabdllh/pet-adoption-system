import openpyxl, json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Pet, PetImage
from .forms import PetForm
from login_register.decorators import admin_required, adopter_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

@login_required
@adopter_required
def adopter_pet_list(request):
    today = timezone.now().date()

    query = request.GET.get('q', '')
    pet_type = request.GET.get('pet_type', '')
    gender = request.GET.get('gender', '')
    status = request.GET.get('status', '')
    age = request.GET.get('age', '')
    adoption_fee_min = request.GET.get('adoption_fee_min', '')
    adoption_fee_max = request.GET.get('adoption_fee_max', '')
    time_in_shelter_min = request.GET.get('time_in_shelter_min', '')
    time_in_shelter_max = request.GET.get('time_in_shelter_max', '')
    sort_by_name = request.GET.get('sort_by_name', '')
    sort_by_age = request.GET.get('sort_by_age', '')
    sort_by_time_in_shelter = request.GET.get('sort_by_time_in_shelter', '')
    sort_by_adoption_fee = request.GET.get('sort_by_adoption_fee', '')

    reset_filter = request.GET.get('reset_filter', False)
    reset_sort = request.GET.get('reset_sort', False)

    # reset logic
    if reset_filter:
        query = ''
        pet_type = ''
        gender = ''
        age = ''
        adoption_fee_min = ''
        adoption_fee_max = ''
        time_in_shelter_min = ''
        time_in_shelter_max = ''
    if reset_sort:
        sort_by_name = ''
        sort_by_age = ''
        sort_by_time_in_shelter = ''
        sort_by_adoption_fee = '' 

    pets = Pet.objects.filter(is_available=True)

    # filters
    if query:
        pets = pets.filter(
            Q(name__icontains=query) |
            Q(pet_type__iexact=query) |
            Q(breed__icontains=query) |
            Q(gender__iexact=query)
        )
    
    if pet_type:
        pets = pets.filter(pet_type__iexact=pet_type)
    if gender:
        if gender == 'none':
            pets = pets.filter(gender__isnull=True)
        else:
            pets = pets.filter(gender__iexact=gender)
    if age:
        pets = pets.filter(age=age)
    if adoption_fee_min:
        pets = pets.filter(adoption_fee__gte=adoption_fee_min)
    if adoption_fee_max:
        pets = pets.filter(adoption_fee__lte=adoption_fee_max)
    if time_in_shelter_min:
        pets = pets.filter(time_in_shelter__gte=time_in_shelter_min)
    if time_in_shelter_max:
        pets = pets.filter(time_in_shelter__lte=time_in_shelter_max)

    # sorting
    if sort_by_name:
        pets = pets.order_by('name' if sort_by_name == 'asc' else '-name')
    if sort_by_age:
        pets = pets.order_by('age' if sort_by_age == 'asc' else '-age')
    if sort_by_time_in_shelter:
        pets = pets.order_by('time_in_shelter' if sort_by_time_in_shelter == 'asc' else '-time_in_shelter')
    if sort_by_adoption_fee:
        pets = pets.order_by('adoption_fee' if sort_by_adoption_fee == 'asc' else '-adoption_fee')

    return render(request, 'adopter_pet_list.html', {
        'pets': pets,
        'query': query,
        'pet_type': pet_type,
        'gender': gender,
        'status': status,
        'age': age,
        'adoption_fee_min': adoption_fee_min,
        'adoption_fee_max': adoption_fee_max,
        'time_in_shelter_min': time_in_shelter_min,
        'time_in_shelter_max': time_in_shelter_max,
        'today': today,
        'sort_by_name': sort_by_name,
        'sort_by_age': sort_by_age,
        'sort_by_time_in_shelter': sort_by_time_in_shelter,
        'sort_by_adoption_fee': sort_by_adoption_fee,
    })

@login_required
def view_pet_detail(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    return render(request, 'view_pet.html', {'pet': pet})

@login_required
@admin_required
def admin_pet_list(request):
    today = timezone.now().date()

    query = request.GET.get('q', '')
    pet_type = request.GET.get('pet_type', '')
    gender = request.GET.get('gender', '')
    status = request.GET.get('status', '')
    age = request.GET.get('age', '')
    adoption_fee_min = request.GET.get('adoption_fee_min', '')
    adoption_fee_max = request.GET.get('adoption_fee_max', '')
    time_in_shelter_min = request.GET.get('time_in_shelter_min', '')
    time_in_shelter_max = request.GET.get('time_in_shelter_max', '')
    sort_by_id = request.GET.get('sort_by_id', '')
    sort_by_name = request.GET.get('sort_by_name', '')
    sort_by_age = request.GET.get('sort_by_age', '')
    sort_by_time_in_shelter = request.GET.get('sort_by_time_in_shelter', '')
    sort_by_adoption_fee = request.GET.get('sort_by_adoption_fee', '')

    reset_filter = request.GET.get('reset_filter', False)
    reset_sort = request.GET.get('reset_sort', False)

    # reset logic
    if reset_filter:
        query = ''
        pet_type = ''
        gender = ''
        age = ''
        adoption_fee_min = ''
        adoption_fee_max = ''
        time_in_shelter_min = ''
        time_in_shelter_max = ''
    if reset_sort:
        sort_by_id = ''
        sort_by_name = ''
        sort_by_age = ''
        sort_by_time_in_shelter = ''
        sort_by_adoption_fee = '' 

    pet_type_choices = Pet.PET_TYPE_CHOICES

    pets = Pet.objects.all()

    # Filtering
    if query:
        pets = pets.filter(
            Q(name__icontains=query) | 
            Q(pet_type__iexact=query) |  
            Q(breed__icontains=query) |  
            Q(gender__iexact=query)
        )

    if pet_type:
        pets = pets.filter(pet_type__iexact=pet_type)
    if gender:
        if gender == 'none':
            pets = pets.filter(gender__isnull=True)
        else:
            pets = pets.filter(gender__iexact=gender)
    if age:
        pets = pets.filter(age__exact=age)
    if adoption_fee_min:
        pets = pets.filter(adoption_fee__gte=adoption_fee_min)
    if adoption_fee_max:
        pets = pets.filter(adoption_fee__lte=adoption_fee_max)
    if time_in_shelter_min:
        pets = pets.filter(time_in_shelter__gte=time_in_shelter_min)
    if time_in_shelter_max:
        pets = pets.filter(time_in_shelter__lte=time_in_shelter_max)

    if status == 'adopted':
        pets = pets.filter(is_adopted=True, is_requested=False, is_rejected=False)
    elif status == 'available':
        pets = pets.filter(is_available=True, is_requested=False, is_rejected=True)
    else:
        pets = pets.filter(is_requested=False)

    # Sorting
    if sort_by_id:
        if sort_by_id == 'asc':
            pets = pets.order_by('id')
        elif sort_by_id == 'desc':
            pets = pets.order_by('-id')

    if sort_by_name:
        if sort_by_name == 'asc':
            pets = pets.order_by('name')
        elif sort_by_name == 'desc':
            pets = pets.order_by('-name')

    if sort_by_age:
        if sort_by_age == 'asc':
            pets = pets.order_by('age')
        elif sort_by_age == 'desc':
            pets = pets.order_by('-age')

    if sort_by_time_in_shelter:
        if sort_by_time_in_shelter == 'asc':
            pets = pets.order_by('time_in_shelter')
        elif sort_by_time_in_shelter == 'desc':
            pets = pets.order_by('-time_in_shelter')

    if sort_by_adoption_fee:
        if sort_by_adoption_fee == 'asc':
            pets = pets.order_by('adoption_fee')
        elif sort_by_adoption_fee == 'desc':
            pets = pets.order_by('-adoption_fee')
    return render(request, 'admin_pet_list.html', {
        'pets': pets,
        'query': query,
        'pet_type': pet_type,
        'pet_type_choices': pet_type_choices, 
        'gender': gender,
        'status': status,
        'age': age,
        'adoption_fee_min': adoption_fee_min,
        'adoption_fee_max': adoption_fee_max,
        'time_in_shelter_min': time_in_shelter_min,
        'time_in_shelter_max': time_in_shelter_max,
        'today': today,
        'sort_by_id': sort_by_id,
        'sort_by_name': sort_by_name,
        'sort_by_age': sort_by_age,
        'sort_by_time_in_shelter': sort_by_time_in_shelter,
        'sort_by_adoption_fee': sort_by_adoption_fee,
    })

@login_required
@admin_required
def admin_add_pet(request):
    if request.method == 'POST':
        pet_form = PetForm(request.POST, request.FILES)
        images = request.FILES.getlist('images')

        if len(images) > 5:
            messages.error(request, "You can only upload a maximum of 5 images.")
            return redirect('admin_pet_list')
        
        if pet_form.is_valid():
            pet = pet_form.save()

            if pet.is_available == False:
                pet.is_adopted = True
            else:
                pet.is_adopted = False

            for i, image in enumerate(images):
                pet_image = PetImage(pet=pet, image=image)
                pet_image.save()
                if i == 0:
                    pet.main_image = pet_image.image
                    pet.save()
            messages.success(request, 'Pet successfully added!')
            return redirect('admin_pet_list')
        else:
            messages.error(request, 'There was an error adding the pet.')
    else:
        pet_form = PetForm()
    return render(request, 'admin_pet_list.html', {'pet_form': pet_form})

@login_required
@admin_required
def admin_edit_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)

    if request.method == 'POST' and 'validation_error' in request.POST:
        validation_error = request.POST['validation_error']
        messages.error(request, validation_error)
        return redirect('admin_pet_list')

    if request.method == 'POST':
        pet_form = PetForm(request.POST, request.FILES, instance=pet)
        images = request.FILES.getlist('images')

        if len(images) > 5:
            messages.error(request, "You can only upload a maximum of 5 images.")
            return redirect('admin_pet_list')

        if pet_form.is_valid():
            pet = pet_form.save()

            if not pet.is_available:
                pet.is_adopted = True
            else:
                pet.is_adopted = False

            for i, image in enumerate(images):
                if i >= 5: 
                    raise ValidationError(_('You can upload a maximum of 5 images.'))
                pet_image = PetImage.objects.create(pet=pet, image=image)

                if i == 0 and not pet.main_image:
                    pet.main_image = pet_image.image

            # set the first new one as main_image
            remaining_images = pet.images.all()
            if remaining_images.exists():
                pet.main_image = remaining_images.first().image
            else:
                pet.main_image = None

            pet.save()

            messages.success(request, 'Pet updated successfully.')
            return redirect('admin_pet_list')
        else:
            messages.error(request, 'There was an error updating the pet.')
    else:
        pet_form = PetForm(instance=pet)

    return render(request, 'admin_pet_list.html', {'pet_form': pet_form, 'pet': pet})

@login_required
@admin_required
def admin_view_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    return render(request, 'admin_view_pet.html', {'pet': pet})

@login_required
@admin_required
def admin_delete_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    pet.delete()
    messages.success(request, 'Pet successfully deleted!')
    return redirect('admin_pet_list')

@login_required
@admin_required
def delete_pet_image(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            image_ids = data.get('image_ids', [])

            if not image_ids:
                return JsonResponse({'success': False, 'error': 'No image IDs provided.'})

            for image_id in image_ids:
                pet_image = get_object_or_404(PetImage, id=image_id)
                pet_image.delete()

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})
       
@login_required
@admin_required
def export_pets_to_excel(request):
    query = request.GET.get('q', '')
    pet_type = request.GET.get('pet_type', '')
    gender = request.GET.get('gender', '')
    sort_by = request.GET.get('sort_by', '')

    pets = Pet.objects.all()
    if query:
        pets = pets.filter(name__icontains=query)
    if pet_type:
        pets = pets.filter(pet_type__iexact=pet_type)
    if gender:
        pets = pets.filter(gender__iexact=gender)
    pets = pets.order_by(sort_by or 'id')

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Pet List"

    # header row
    ws.append(['ID', 'Pet Name', 'Species', 'Breed', 'Age', 'Gender', 'Adoption Fee', 'Time in Shelter', 'Status'])

    # pet data rows
    for pet in pets:
        ws.append([pet.id, pet.name, pet.pet_type, pet.breed, pet.age, pet.gender, pet.adoption_fee, pet.time_in_shelter, 'Available' if pet.is_available else 'Adopted'])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="pet_list.xlsx"'
    wb.save(response)

    return response