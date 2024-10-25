from django.urls import path
from .views import schedule, success

urlpatterns = [
    path('<int:pet_id>/', schedule, name='schedule'),
     path('success/', success, name='success'),  # Add this line
]