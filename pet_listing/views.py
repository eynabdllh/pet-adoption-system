from django.shortcuts import render, get_object_or_404
from .models import Pet

def adopter_pet_list(request):
    pets = Pet.objects.all() 
    return render(request, 'adopter_pet_list.html', {'pets': pets})

def view_pet_detail(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    return render(request, 'view_pet.html', {'pet': pet})