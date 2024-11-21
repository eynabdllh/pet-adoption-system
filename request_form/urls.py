from django.urls import path
from .views import adopt_form, adoption_management, review_form, admin_pickup

urlpatterns = [
    path('<int:pet_id>/', adopt_form, name='adopt_form'),
    path('adoption_management/', adoption_management, name='adoption_management'),
    path('review_form/<int:pet_id>/', review_form, name='review_form'),
    path('admin_pickup/', admin_pickup, name='admin_pickup'),
]