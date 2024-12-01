from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password, make_password
from .forms import LoginForm, RegisterForm
from .models import User
from profile_management.models import Profile
from django.contrib import messages
from notifications.models import Notification
from django.utils import timezone

def Login(request):
    validation_error = None

    if 'user_id' in request.session:
        user = User.objects.get(id = request.session.get('user_id'))
        return redirect('admin_dashboard' if user.isAdmin else 'adopter_dashboard')

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

                Notification.objects.filter(
                    user=user,
                    created_at__lte=timezone.now() - timezone.timedelta(days=30),
                    isRead=False
                ).update(isRead=True)

                next_url = request.GET.get('next', 'admin_dashboard' if user.isAdmin else 'adopter_dashboard')
                return redirect(next_url)
                
            else:
                messages.error(request, 'Invalid email or password.')
    else:
        #messages.default_app_config
        if request.session.get('remember_me',None) == True:
            form = LoginForm(initial={'remember_me': True, 'email': request.session.get('saved_user_email',None), 'password': request.session.get('saved_user_password',None)})
        else:
            form = LoginForm()

    return render(request, 'login.html', {
        'form': form,
        # 'validation': validation_error,
    })

def Register(request): 
    validation_error = None

    if 'user_id' in request.session:
        user = User.objects.get(id = request.session.get('user_id'))
        return redirect('admin_dashboard' if user.isAdmin else 'adopter_dashboard')

    if request.method == "POST":
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            user = form.save()

            if user.isAdmin:
                Notification.objects.create_for_adopter(
                    adopter=user,
                    title="Welcome to Admin Panel",
                    message="Welcome to Adopt-a-Pet! You've been registered as an admin. You can now manage pets, adoptions, and more."
                )
            else:
                Notification.objects.create_for_adopter(
                    adopter=user,
                    title="Welcome to Adopt-a-Pet",
                    message=(
                        "Welcome to Adopt-a-Pet! 🐾\n\n"
                        "Here's what you can do: \n"
                        "• Browse available pets\n"
                        "• Submit adoption requests\n"
                        "• Schedule pet pickups\n"
                        "• Track your adoption status\n\n"
                        "Start your journey by exploring our available pets!"
                    )
                )

            messages.success(request, "Registration successful!")
            return redirect('login') 
        else:
            messages.error(request, 'Please correct the errors above.')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {
        'form': form,
        'validation': validation_error,
    })

def logout(request):
    if 'user_id' in request.session:
        user = User.objects.get(id=request.session['user_id'])
        
        del request.session['user_id']
    if 'user_type' in request.session:
        del request.session['user_type']

    if request.session.get('remember_me',None) == False and 'saved_user_email' in request.session and 'saved_user_password' in request.session:
        del request.session['saved_user_email']
        del request.session['saved_user_password']

    return redirect('login')

def landing_page(request):
    return render(request, 'landing_page.html')