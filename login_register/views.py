from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password, make_password
from .forms import LoginForm, RegisterForm
from .models import User
from profile_management.models import Profile

def Login(request):
    validation_error = None

    if request.method == "POST":
        form = LoginForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data['remember_me']

            user = User.objects.filter(email=email).first()

            if user and check_password(password, user.password):
                request.session['user_id'] = user.id
                request.session['user_type'] = 'Admin' if user.isAdmin else 'Adopter'
                request.session['user_first_name'] = user.first_name
                request.session['user_last_name'] = user.last_name
                request.session['remember_me'] =  True if remember_me else False

                profile = Profile.objects.filter(user=user).first()
                request.session['profile_image_url'] = profile.profile_image.url if profile and profile.profile_image else None

                next_url = request.GET.get('next', 'admin_pet_list' if user.isAdmin else 'adopter_pet_list')
                return redirect(next_url)
               
            else:
                validation_error = 'Invalid email or password.'
    else:
        if request.session.get('remember_me',None) == True:
            id = request.session['user_id']
            user = User.objects.get(id=id)
            form = LoginForm(initial={'remember_me': True, 'email': user.email, 'password': "tf man"})

        else:
            form = LoginForm()

    return render(request, 'login.html', {
        'form': form,
        'validation': validation_error,
    })

def Register(request): 
    validation_error = None

    if request.method == "POST":
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('login') 
        else:
            validation_error = "Please correct the errors above."
    else:
        form = RegisterForm()

    return render(request, 'register.html', {
        'form': form,
        'validation': validation_error,
    })


def logout(request):
    remember_me = request.session['remember_me']

    if 'user_id' in request.session and not remember_me:
        del request.session['user_id']
    if 'user_type' in request.session:
        del request.session['user_type']

    return redirect('login')