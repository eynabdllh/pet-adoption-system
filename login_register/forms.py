from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Password",widget=forms.PasswordInput)

class RegisterForm(forms.Form):
    first_name = forms.CharField(label="First Name")
    last_name = forms.CharField(label="Last Name")
    age = forms.IntegerField(label='Age')
    contact_no = forms.CharField(max_length=11)
    address = forms.CharField(max_length=100)
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Password",widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="Confirm Password",widget=forms.PasswordInput)