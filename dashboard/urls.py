from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.adopter_dashboard, name='adopter_dashboard'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('pet/<int:pet_id>/', views.view_pet_detail, name='view_pet_detail'),
    path('review_form/<int:pet_id>/', views.review_form_detail, name='review_form_detail'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)