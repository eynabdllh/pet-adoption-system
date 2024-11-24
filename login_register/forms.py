from django import forms
from django.contrib.auth.hashers import make_password
from .models import User

class LoginForm(forms.Form):
    email = forms.EmailField(label="Email Address", widget=forms.TextInput(attrs={'class': 'form-text'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-text'}))
    remember_me = forms.BooleanField(label="Remember Me", initial=False ,required=False, label_suffix="", widget=forms.CheckboxInput(attrs={'class': 'form-checkbox'}))

class RegisterForm(forms.ModelForm):
    full_name = forms.CharField(label="Full Name", max_length=100, widget=forms.TextInput(attrs={'class': 'form-text'}))
    email = forms.EmailField(label="Email", widget=forms.TextInput(attrs={'class': 'form-text'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-text'}))
    confirm_password = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'class': 'form-text'}))

    class Meta:
        model = User
        fields = ['full_name', 'email', 'password'] 
        widgets = {
            'password': forms.PasswordInput(), 
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match.')
        else:
            cleaned_data['password'] = make_password(password) 
        return cleaned_data

    def save(self, commit=True):
        full_name = self.cleaned_data.get('full_name')
        first_name, last_name = self.split_full_name(full_name)

        user = super().save(commit=False)
        user.first_name = first_name
        user.last_name = last_name

        if commit:
            user.save()
        return user
    
    @staticmethod
    def split_full_name(full_name):
        parts = full_name.split()
        first_name = ' '.join(parts[:-1])
        last_name = parts[-1]
       
        return first_name, last_name