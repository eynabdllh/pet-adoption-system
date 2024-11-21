from django.urls import path
from .views import notification_list

urlpatterns = [
    path('', notification_list, name='notification_list'),
]