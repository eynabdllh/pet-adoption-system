from django.urls import path
from .views import adopt_form, adoption_management

urlpatterns = [
    path('<int:pet_id>/', adopt_form, name='adopt_form'),
    path('adoption_management/', adoption_management, name='adoption_management'),
]