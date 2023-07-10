from django.urls import path
from .views import User_Sign_Up, User_Log_In, User_Log_Out, User_Info

urlpatterns = [
    path("signup/", User_Sign_Up.as_view()),
    path("login/", User_Log_In.as_view()),
    path("logout/", User_Log_Out.as_view()),
    path("info/", User_Info.as_view()),
]
