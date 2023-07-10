from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
)
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import App_User

# Create your views here.


class User_Sign_Up(ObtainAuthToken):
    def post(self, request):
        print(request.data)
        request.data["username"] = request.data["email"]
        user = App_User.objects.create_user(**request.data)
        token = Token.objects.create(user=user)
        return Response(
            {"token": token.key, "user": {"id": user.pk, "email": user.email, "name":user.preferred_name}},
            status=HTTP_201_CREATED,
        )


class User_Log_In(ObtainAuthToken):
    def post(self, request):
        print("LOGIN", request.data)
        user = authenticate(
            username=request.data["email"], password=request.data["password"]
        )
        if user:
            token = Token.objects.create(user=user)
            login(request, user)
            return Response({"token": token.key, "user": {"id": user.pk, "email": user.email, "name":user.preferred_name}})
        else:
            return Response("No user matching creadentials", status=HTTP_404_NOT_FOUND)


class User_Log_Out(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        logout(request)
        return Response(status=HTTP_204_NO_CONTENT)


class User_Info(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            {"email": request.user.email, "name": request.user.preferred_name}
        )

    def put(self, request):
        user = request.user
        data = request.data
        success = []
        if "preferred_name" in data:
            user.preferred_name = data["preferred_name"]
            success.append("preferred_name")
        if "password" in data and authenticate(
            username=user.email, password=data["old_password"]
        ) == request.user:
            user.set_password(data["password"])
            success.append("password")
        user.save()
        return Response(
            f"{', '.join(success)} have been updated",
            status=HTTP_200_OK,
        )
