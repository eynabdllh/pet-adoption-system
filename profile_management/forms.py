from django import forms
from login_register.models import User
from .models import Profile

class UserUpdateForm(forms.ModelForm):
    new_password = forms.CharField(max_length=255, required=False, widget=forms.PasswordInput, label='New Password')
    confirm_password = forms.CharField(max_length=255, required=False, widget=forms.PasswordInput, label='Confirm New Password')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'new_password', 'confirm_password']
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_image', 'age', 'address', 'phone_number']