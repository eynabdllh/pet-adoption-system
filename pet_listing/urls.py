from django.urls import path
from . import views

urlpatterns = [
    path('', views.adopter_pet_list, name='adopter_pet_list'),
    path('<int:pet_id>/', views.view_pet_detail, name='view_pet'),
]
