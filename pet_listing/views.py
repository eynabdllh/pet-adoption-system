from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse
from .models import Pet, PetImage
from .forms import PetForm, PetImageFormSet

def adopter_pet_list(request):
    query = request.GET.get('q', '')
    pets = Pet.objects.all() 
    if query:
        pets = pets.filter(name__icontains=query)
    return render(request, 'adopter_pet_list.html', {'pets': pets , 'query': query,})

def view_pet_detail(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    return render(request, 'view_pet.html', {'pet': pet})

def admin_pet_list(request):
    query = request.GET.get('q', '')  
    pets = Pet.objects.filter(name__icontains=query) if query else Pet.objects.all()
    return render(request, 'admin_pet_list.html', {'pets': pets, 'query': query})

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
            return redirect('admin_pet_list')
    else:
        pet_form = PetForm()
    return render(request, 'admin_add_pet.html', {'pet_form': pet_form})

def admin_edit_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    
    if request.method == 'POST':
        pet_form = PetForm(request.POST, request.FILES, instance=pet)
        images_formset = PetImageFormSet(request.POST, request.FILES, instance=pet)
        
        if pet_form.is_valid() and images_formset.is_valid():
            pet = pet_form.save(commit=False)
            
            images_formset.save()

            # Handle the main image
            if images_formset.cleaned_data:
                new_images = pet.images.all()
                if new_images.exists():
                    pet.main_image = new_images.first().image

            pet.save()

            return redirect('admin_pet_list')

    else:
        pet_form = PetForm(instance=pet)
        images_formset = PetImageFormSet(instance=pet)

    return render(request, 'admin_edit_pet.html', {
        'pet_form': pet_form,
        'images_formset': images_formset,
        'pet': pet,
    })

def admin_view_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    return render(request, 'admin_view_pet.html', {'pet': pet})

def admin_delete_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    pet.delete()
    return redirect('admin_pet_list')

def admin_pet_list(request):
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
        if gender == 'none':
            pets = pets.filter(gender__isnull=True)
        else:
            pets = pets.filter(gender__iexact=gender)

    if sort_by:
        pets = pets.order_by(sort_by)
    else:
        pets = pets.order_by('id')  

    return render(request, 'admin_pet_list.html', {
        'pets': pets,
        'query': query,
        'pet_type': pet_type,
        'gender': gender,
        'sort_by': sort_by,
    })