from django.shortcuts import render, get_object_or_404
from django.core.serializers import serialize
from django.utils import timezone
from .models import Post, Comment, Reply
from user_app.models import App_User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
    HTTP_500_INTERNAL_SERVER_ERROR
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from datetime import datetime, timedelta
import json


# Create your views here.
class View_Posts(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post_formatter(self, post):
        json_post = json.loads(
            serialize("json", [post], fields=["user", "likes", "content"])
        )
        data = json_post[0]["fields"]
        data["id"] = json_post[0]["pk"]
        user = get_object_or_404(App_User, id=data["user"])
        data["user"] = user.preferred_name
        data["user_email"] = user.email
        data["comments"] = Comment.objects.filter(parent_post=post)
        return data

    def post(self, request):
        try:
            data = {"user": request.user, "content": request.data["content"]}
            new_post = Post.objects.create(**data)
            new_post.save()
            post = self.post_formatter(new_post)
            return Response({"created": True, "post": post}, status=HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({"created": False}, status=HTTP_400_BAD_REQUEST)
        
    def get(self, request):
        try:
            today = timezone.now()
            yesterday = today - timedelta(days=1)
            posts = Post.objects.filter(date_created__range=[yesterday, today]).order_by('-date_created')
            posts = [self.post_formatter(x) for x in posts]
            return Response(posts)
        except Exception as e:
            print(e)
            return Response("Something went wrong", status=HTTP_500_INTERNAL_SERVER_ERROR)


class View_A_Post(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        post = get_object_or_404(Post, id=id)
        if post.user == request.user:
            post.delete()
            return Response({"deleted": True}, status=HTTP_200_OK)
        else:
            return Response("Not your post", status=HTTP_401_UNAUTHORIZED)

    def put(self, request, id):
        try:
            post = get_object_or_404(Post, id=id)
            if "content" in request.data:
                post.content = request.data["content"]
                post.save()
                return Response({"updated": True, "new_content": post.content})
            if "liked" in request.data:
                if request.data["liked"]:
                    post.liked()
                else:
                    post.unliked()
                post.save()
                return Response({"updated": True, "likes": post.likes})
            return Response(status=HTTP_204_NO_CONTENT)
        except Exception as e:
            print(e)
            return Response({"updated": False}, status=HTTP_400_BAD_REQUEST)

    def get(self, request, id):
        post = get_object_or_404(Post, id=id)
        data = self.post_formatter(post)
        return Response(data)


class View_All_My_Posts(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post_formatter(self, post):
        json_post = json.loads(
            serialize("json", [post], fields=["user", "likes", "content"])
        )
        data = json_post[0]["fields"]
        data["id"] = json_post[0]["pk"]
        data["user"] = get_object_or_404(App_User, id=data["user"]).preferred_name
        return data

    def get(self, request):
        try:
            my_posts = Post.objects.filter(user=request.user)
            my_posts = [self.post_formatter(post) for post in my_posts]
            return Response({"my_posts": my_posts})
        except Exception as e:
            return Response("Something went wrong", status=HTTP_400_BAD_REQUEST)


class View_A_Comment(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, id):
        try:
            comment = get_object_or_404(Comment, id=id)
            if "content" in request.data:
                comment.content = request.data["content"]
                comment.save()
                return Response({"updated": True, "new_content": comment.content})
            if "liked" in request.data:
                if request.data["liked"]:
                    comment.liked()
                else:
                    comment.unliked()
                comment.save()
                return Response({"updated": True, "likes": comment.likes})
            return Response(status=HTTP_204_NO_CONTENT)
        except Exception as e:
            print(e)
            return Response({"updated": False}, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        comment = get_object_or_404(Comment, id=id)
        comment.parent_post.comments -= 1
        comment.delete()
        return Response({"deleted": True}, status=HTTP_200_OK)


class Create_or_Get_Comments(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def format_comment(self, comment):
        json_comment = json.loads(serialize("json", [comment]))
        data = json_comment[0]["fields"]
        data["id"] = json_comment[0]["pk"]
        data["user"] = get_object_or_404(App_User, id = data["user"]).preferred_name
        return data

    def get(self, request, id):
        post = get_object_or_404(Post, id=id)
        comments = Comment.objects.filter(parent_post=post)
        comments = [self.format_comment(comment) for comment in comments]
        return Response({"comments": comments})

    def post(self, request, id):
        post = get_object_or_404(Post, id=id)
        data = request.data
        data["user"] = request.user
        data["parent_post"] = post
        post.comments += 1
        comment = Comment.objects.create(**data)
        comment.save()
        return Response(
            {"created": True, "comment": self.format_comment(comment)},
            status=HTTP_201_CREATED,
        )
