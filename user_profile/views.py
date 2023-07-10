from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Profile
from django.core.serializers import serialize
import json


# Create your views here.
class User_Profile(APIView):
    authentication_classes= [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile, create = Profile.objects.get_or_create(user = request.user)
        json_profile = json.loads(serialize("json", [profile]))
        profile = json_profile[0]["fields"]
        profile["user"] = request.user.preferred_name
        list_return = []
        for key, val in profile.items():
            list_return.append({"title":key,"body":val})
        return Response(list_return)
    
    def put(self, request):
        print("\n from request \n",request.data)
        profile = Profile.objects.get(user = request.user)
        if "years_of_xp" in request.data:
            profile.years_of_xp = request.data["years_of_xp"]
        if "job_title" in request.data:
            profile.job_title = request.data["job_title"]
        if "profession" in request.data:
            profile.profession = request.data["profession"]
        if "employer" in request.data:
            profile.employer = request.data["employer"]
        if "bio" in request.data:
            profile.bio = request.data["bio"]
        profile.save()
        if "user" in request.data:
            request.user.preferred_name = request.data["user"]
            request.user.save()
        print(json.loads(serialize("json",[profile])))
        return Response(status=HTTP_204_NO_CONTENT)