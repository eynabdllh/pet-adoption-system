from django.urls import path
from . import views 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.adopter_profile_view, name='adopter_profile_view'),
    path('admin/', views.admin_profile_view, name='admin_profile_view'),
    path('delete-image/', views.delete_profile_image, name='delete_profile_image'),
    path('upload_image/', views.upload_profile_image, name='upload_profile_image'), 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)