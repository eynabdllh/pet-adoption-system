# forms.py

from django import forms
from .models import Adoption
from django.utils import timezone

class AdoptionForm(forms.ModelForm):
    adopter_id = forms.CharField(label='Adopter ID', required=False, widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = Adoption
        fields = ['adopter_id', 'first_name', 'last_name', 'age', 'address', 'contact_number', 'email', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'value': timezone.now().date()}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        profile = kwargs.pop('profile', None)
        super(AdoptionForm, self).__init__(*args, **kwargs)

        # Set readonly for adopter_id
        if user:
            self.fields['adopter_id'].initial = user.id

        # Set today's date if this is a new instance
        if not self.instance.pk:
            self.fields['date'].initial = timezone.now().date()
        self.fields['date'].widget.attrs['value'] = timezone.now().date().strftime('%Y-%m-%d')

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age is not None and (not isinstance(age, int) or age < 0):
            raise forms.ValidationError("Please enter a valid non-negative integer for age.")
        return age
