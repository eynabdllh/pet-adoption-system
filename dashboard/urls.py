from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)