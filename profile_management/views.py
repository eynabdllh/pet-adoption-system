from django.shortcuts import render

def adopter_profile_view(request):
    return render(request, 'adopter_profile.html')
