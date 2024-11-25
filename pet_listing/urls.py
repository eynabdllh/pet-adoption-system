from django.urls import path
from . import views

urlpatterns = [
    path('admin-dashboard/', views.admin_pet_list, name='admin_pet_list'),
    path('admin-dashboard/add/', views.admin_add_pet, name='admin_add_pet'),
    path('admin-dashboard/<int:pet_id>/', views.admin_view_pet, name='admin_view_pet'),
    path('admin-dashboard/update/<int:pet_id>/', views.admin_edit_pet, name='admin_edit_pet'),
    path('admin-dashboard/delete/<int:pet_id>/', views.admin_delete_pet, name='admin_delete_pet'),
    path('', views.adopter_pet_list, name='adopter_pet_list'),
    path('<int:pet_id>/', views.view_pet_detail, name='view_pet'),
    path('admin/pets/export/', views.export_pets_to_excel, name='export_pets_to_excel'),
    path('delete_pet_image/', views.delete_pet_image, name='delete_pet_image'),
]