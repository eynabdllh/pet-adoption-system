from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserUpdateForm, ProfileUpdateForm
from login_register.models import User  

@login_required
def adopter_profile_view(request):
    current_user_id = request.session.get('user_id')
    current_user = User.objects.get(id=current_user_id)

    if current_user.isAdmin:
        return redirect('admin_profile_view')

    profile = current_user.profile

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=current_user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            if new_password and new_password != confirm_password:
                messages.error(request, 'New password and confirm password do not match.')
            else:
                if new_password:
                    current_user.set_password(new_password)

                user_form.save()
                profile_form.save()

                request.session['user_first_name'] = user_form.cleaned_data['first_name']
                request.session['user_last_name'] = user_form.cleaned_data['last_name']
                request.session['profile_image_url'] = profile.profile_image.url if profile.profile_image else None

                messages.success(request, 'Your profile has been updated!')

                return redirect('adopter_profile_view')
        else:
            messages.error(request, 'Error! Please check the details and try again.')

    else:
        user_form = UserUpdateForm(instance=current_user)
        profile_form = ProfileUpdateForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile': profile,
        'profile_form': profile_form,
    }
    return render(request, 'adopter_profile.html', context)


@login_required
def admin_profile_view(request):
    current_user_id = request.session.get('user_id')
    current_user = User.objects.get(id=current_user_id)

    if not current_user.isAdmin:
        return redirect('adopter_profile_view')

    profile = current_user.profile

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=current_user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            if new_password and new_password != confirm_password:
                messages.error(request, 'New password and confirm password do not match.')
            else:
                if new_password:
                    current_user.set_password(new_password)

                user_form.save()
                profile_form.save()

                request.session['user_first_name'] = user_form.cleaned_data['first_name']
                request.session['user_last_name'] = user_form.cleaned_data['last_name']
                request.session['profile_image_url'] = profile.profile_image.url if profile.profile_image else None

                messages.success(request, 'Your profile has been updated!')

                return redirect('admin_profile_view')
        else:
            messages.error(request, 'Error! Please check the details and try again.')
    else:
        user_form = UserUpdateForm(instance=current_user)
        profile_form = ProfileUpdateForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile': profile,
        'profile_form': profile_form,
    }
    return render(request, 'admin_profile.html', context)


@login_required
def upload_profile_image(request):
    current_user_id = request.session.get('user_id')
    current_user = User.objects.get(id=current_user_id)
    profile = current_user.profile  

    if request.method == 'POST':
        if 'profile_image' in request.FILES:
            profile.profile_image = request.FILES['profile_image']
            profile.save()

            request.session['profile_image_url'] = profile.profile_image.url if profile.profile_image else None

            messages.success(request, 'Profile image updated!')

    if current_user.isAdmin:
        return redirect('admin_profile_view')
    else:
        return redirect('adopter_profile_view')


@login_required
def delete_profile_image(request):
    current_user_id = request.session.get('user_id')
    current_user = User.objects.get(id=current_user_id)
    profile = current_user.profile

    if request.method == 'POST':
        if profile.profile_image:
            profile.profile_image.delete()  
            profile.profile_image = None 
            profile.save()

            request.session['profile_image_url'] = None 
            messages.success(request, 'Profile image has been deleted.')
        else:
            messages.error(request, 'No profile image to delete.')

    if current_user.isAdmin:
        return redirect('admin_profile_view')
    else:
        return redirect('adopter_profile_view')