from django.urls import path
from . import views

urlpatterns = [
    path('', views.notification_list, name='notifications'),
    path('mark-as-read/<int:notification_id>/', views.mark_as_read, name='mark_as_read'),
    path('mark-all-as-read/', views.mark_all_as_read, name='mark_all_as_read'),
    path('remove/<int:notification_id>/', views.remove_notification, name='remove_notification'),
    path('remove-all-read/', views.remove_all_read, name='remove_all_read'),
]