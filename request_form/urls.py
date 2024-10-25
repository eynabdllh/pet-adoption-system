from django.urls import path
from .views import adopt_form, confirmation 

urlpatterns = [
    path('<int:pet_id>/', adopt_form, name='adopt_form'),
    path('confirmation/', confirmation, name='confirmation'),
]