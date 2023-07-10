from django.urls import path
from .views import send_home

urlpatterns = [
    path('', send_home)
]
