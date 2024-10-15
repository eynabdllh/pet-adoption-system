from django.urls import path
from . import views 

urlpatterns = [
    path('', views.adopter_profile_view, name='adopter_profile_view'),
]