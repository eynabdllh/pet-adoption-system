from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.Login, name="login"),
    path('register/', views.Register, name="register"),
    path('logout/', views.logout, name='logout'),
    path('', views.landing_page, name='landing_page'),
]