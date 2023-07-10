from django.urls import path
from .views import User_Profile

urlpatterns = [
    path("", User_Profile.as_view())
]
