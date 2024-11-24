import openpyxl
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Pet, PetImage
from .forms import PetForm
from login_register.decorators import admin_required, adopter_required
from django.contrib import messages
from django.db.models import Q

@login_required
@adopter_required
def adopter_pet_list(request):
    query = request.GET.get('q', '')
    pets = Pet.objects.filter(is_available=True) 
    if query:
        pets = pets.filter(
            Q(name__icontains=query) | 
            Q(pet_type__iexact=query) |  
            Q(breed__icontains=query) |  
            Q(gender__iexact=query)
        )
    return render(request, 'adopter_pet_list.html', {'pets': pets, 'query': query})

@login_required
def view_pet_detail(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    return render(request, 'view_pet.html', {'pet': pet})

@login_required
@admin_required
def admin_pet_list(request):
    query = request.GET.get('q', '')
    pet_type = request.GET.get('pet_type', '')
    gender = request.GET.get('gender', '')
    sort_by = request.GET.get('sort_by', '')

    pets = Pet.objects.all()
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
    pets = pets.order_by(sort_by or 'id')

    return render(request, 'admin_pet_list.html', {
        'pets': pets,
        'query': query,
        'pet_type': pet_type,
        'gender': gender,
        'sort_by': sort_by,
    })

@login_required
@admin_required
def admin_add_pet(request):
    if request.method == 'POST':
        pet_form = PetForm(request.POST, request.FILES)
        images = request.FILES.getlist('images')
        if pet_form.is_valid():
            pet = pet_form.save()
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
    if request.method == 'POST':
        pet_form = PetForm(request.POST, request.FILES, instance=pet)

        if pet_form.is_valid():
            pet = pet_form.save()
            for image in request.FILES.getlist('images'):
                PetImage.objects.create(pet=pet, image=image)

            messages.success(request, 'Pet updated successfully.')
            return redirect('admin_pet_list')
        else:
            messages.error(request, 'There was an error updating the pet.')
    else:
        pet_form = PetForm(instance=pet)

    return render(request, 'admin_pet_list.html', {
        'pet_form': pet_form,
        'pet': pet,
    })

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