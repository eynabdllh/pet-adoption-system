from django.urls import path
from .views import schedule, success, pickup_list

urlpatterns = [
    path('<int:pet_id>/', schedule, name='schedule'),
     path('success/', success, name='success'),  
     path('pickup_list/', pickup_list, name='pickup_list'),
]