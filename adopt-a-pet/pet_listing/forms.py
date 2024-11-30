from django import forms
from .models import Pet, PetImage
from django.forms.models import inlineformset_factory

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['name', 'age', 'pet_type', 'breed', 'gender', 'adoption_fee', 'is_available', 'main_image', 'time_in_shelter', 'description']


PetImageFormSet = inlineformset_factory(Pet, PetImage, fields=('image',), extra=5, max_num=5)
