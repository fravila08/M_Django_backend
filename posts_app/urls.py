from django.urls import path
from .views import View_Posts, View_A_Post, View_All_My_Posts, View_A_Comment, Create_or_Get_Comments

urlpatterns = [
    path("", View_Posts.as_view()),
    path("<int:id>/", View_A_Post.as_view()),
    path("myposts/", View_All_My_Posts.as_view()),
    path("<int:id>/comments/", Create_or_Get_Comments.as_view()),
    path("comments/<int:id>/", View_A_Comment.as_view()),
]
