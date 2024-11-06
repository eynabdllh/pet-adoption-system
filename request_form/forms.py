from django import forms
from .models import Adoption
from django.utils import timezone
from profile_management.models import Profile 

class AdoptionForm(forms.ModelForm):
    adopter_id = forms.CharField(label='Adopter ID', required=False, widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = Adoption
        fields = ['adopter_id', 'first_name', 'last_name', 'age', 'address', 'contact_number', 'email', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(AdoptionForm, self).__init__(*args, **kwargs)

        if user:
            self.fields['adopter_id'].initial = user.id
            
            try:
                profile = Profile.objects.get(user=user)
                self.fields['first_name'].initial = user.first_name 
                self.fields['last_name'].initial = user.last_name   
                self.fields['age'].initial = profile.age
                self.fields['address'].initial = profile.address
                self.fields['contact_number'].initial = profile.phone_number
                self.fields['email'].initial = user.email          
            except Profile.DoesNotExist:
                pass  

        if not self.instance.pk:
            self.fields['date'].initial = timezone.now().date()
        self.fields['date'].widget.attrs['value'] = timezone.now().date().strftime('%Y-%m-%d')

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age is not None and (not isinstance(age, int) or age < 0):
            raise forms.ValidationError("Please enter a valid non-negative integer for age.")
        return age
