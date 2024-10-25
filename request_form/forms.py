from django import forms
from .models import Adoption
from django.utils import timezone

class AdoptionForm(forms.ModelForm):
    adopter_id = forms.CharField(label='Adopter ID', required=False, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    class Meta:
        model = Adoption
        fields = ['adopter_id','first_name', 'last_name', 'age', 'address', 'contact_number', 'email', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'value': timezone.now().date() }),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(AdoptionForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['adopter_id'].initial = user.id 
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['age'].initial = user.age
            self.fields['address'].initial = user.address
            self.fields['contact_number'].initial = user.contact_no
            self.fields['email'].initial = user.email

        if not self.instance.pk:  # This means the form is for a new instance
            self.fields['date'].initial = timezone.now().date()
        self.fields['date'].widget.attrs['value'] = timezone.now().date().strftime('%Y-%m-%d')  # Format it correctly for the HTML5 date input