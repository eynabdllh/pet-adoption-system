from django.urls import path
from .views import adopt_form 

urlpatterns = [
    path('<int:pet_id>/', adopt_form, name='adopt_form'),
]