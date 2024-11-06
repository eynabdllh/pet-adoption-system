from django.urls import path
from .views import schedule, success, pickup_list, my_adoption, view_details

urlpatterns = [
    path('<int:pet_id>/', schedule, name='schedule'),
     path('success/', success, name='success'),  
     path('pickup_list/', pickup_list, name='pickup_list'),
     path('myadoption/', my_adoption, name='my_adoption'),
     path('viewdetails/<int:user_id>/<int:pet_id>/',view_details, name='view_details'),
]