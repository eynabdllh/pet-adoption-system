from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password, make_password
from .forms import LoginForm, RegisterForm
from .models import User
from profile_management.models import Profile
from django.contrib import messages
from notifications.models import Notification

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
                
                if remember_me:
                    request.session['remember_me'] =  True
                    request.session['saved_user_email'] = email
                    request.session['saved_user_password'] = password   #this one is a potential vulnerability issue as user password is hash stored but this is the only way to store it
                else:
                    request.session['remember_me'] = False

                profile = Profile.objects.filter(user=user).first()
                request.session['profile_image_url'] = profile.profile_image.url if profile and profile.profile_image else None

                next_url = request.GET.get('next', 'admin_dashboard' if user.isAdmin else 'adopter_pet_list')
                #messages.success(request,f"{"Admin" if user.isAdmin else "Adopter"} logged in successfully")
                return redirect(next_url)
               
            else:
                validation_error = 'Invalid email or password.'
                messages.error(request,validation_error)
    else:
        #messages.default_app_config
        if request.session.get('remember_me',None) == True:
            form = LoginForm(initial={'remember_me': True, 'email': request.session.get('saved_user_email',None), 'password': request.session.get('saved_user_password',None)})
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
            Notification.objects.create(user=User.objects.get(email=form.cleaned_data['email']),title="Welcome to Adopt-a-Pet",message="Welcome to our website! You can search for pets you want to adopt.")
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
    if 'user_id' in request.session:
        del request.session['user_id']
    if 'user_type' in request.session:
        del request.session['user_type']

    if request.session.get('remember_me',None) == False and 'saved_user_email' in request.session and 'saved_user_password' in request.session:
        del request.session['saved_user_email']
        del request.session['saved_user_password']

    return redirect('login')