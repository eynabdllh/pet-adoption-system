from django.urls import path
from .views import adopt_form, adoption_management, review_form, admin_pickup, export_adoption_to_excel, export_pickup_to_excel

urlpatterns = [
    path('<int:pet_id>/', adopt_form, name='adopt_form'),
    path('adoption_management/', adoption_management, name='adoption_management'),
    path('review_form/<int:pet_id>/', review_form, name='review_form'),
    path('admin_pickup/', admin_pickup, name='admin_pickup'),
    path('admin/adoption/export/', export_adoption_to_excel, name='export_adoption_to_excel'),
    path('admin/pickup/export/', export_pickup_to_excel, name='export_pickup_to_excel'),
]