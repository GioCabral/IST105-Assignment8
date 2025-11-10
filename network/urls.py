from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('leases/', views.view_leases, name='leases'),
]
