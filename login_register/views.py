from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from .forms import LoginForm, RegisterForm
from .models import User

def Login(request):
    validation_error = None

    if request.method == "POST":
        form = LoginForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = User.objects.filter(email=email).first()

            if user and check_password(password, user.password):
                request.session['user_id'] = user.id
                request.session['user_type'] = 'Admin' if user.isAdmin else 'Adopter'

                next_url = request.GET.get('next', 'admin_pet_list' if user.isAdmin else 'adopter_pet_list')
                return redirect(next_url)
               
            else:
                validation_error = 'Invalid email or password.'
    else:
        form = LoginForm()

    return render(request, 'login.html', {
        'form': form,
        'validation': validation_error,
        'title_text': 'Login',
        'submit_text': 'Log in',
        'redirect_message': "Don't have an account?",
        'redirect_title': 'Sign up',
        'redirect_link': 'register'
    })

def Register(request): 
    validation_error = None

    if request.method == "POST":
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            user = form.save() 
            return redirect('login')  
        else:
            validation_error = "Please correct the errors above."
    else:
        form = RegisterForm()

    return render(request, 'register.html', {
        'form': form,
        'validation': validation_error,
        'title_text': 'Register',
        'submit_text': "Sign up",
        'redirect_message': 'Already have an account?',
        'redirect_title': 'Log in',
        'redirect_link': 'login'
    })

def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    if 'user_type' in request.session:
        del request.session['user_type']

    return redirect('login')