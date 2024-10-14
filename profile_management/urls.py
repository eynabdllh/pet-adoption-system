from django.urls import path
from . import views 

urlpatterns = [
    path('profile/', views.adopter_profile_view, name='adopter_profile_view'),
]