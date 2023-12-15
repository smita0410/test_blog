import uuid

from django.shortcuts import render
from django.db import transaction
from django.db.models import Q, F
from rest_framework import status, generics, filters
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from blogs.blg.models import User, BlogTags, BlogCategories, Blogs, BlogComments
from blogs.blg.serializers import BlogTagsSerializer, BlogCategoriesSerializer, BlogsSerializer, BlogCommentsSerializer


def responsedata(status, message, data=None):
    if status:
        return {"status":status,"message":message,"data":data}
    else:
        return {"status":status,"message":message}


class SignIn(TokenObtainPairView):
    def post(self, request):

        if not request.data.get('password'):
            return Response(responsedata(False, "Password is required"), status=status.HTTP_400_BAD_REQUEST)

        if request.data.get('email'):
            user = User.objects.filter(email=request.data.get('email')).values().first()
            if not user['email_verified']:
                return Response(responsedata(False, "Email not verified"), status=status.HTTP_400_BAD_REQUEST)

        elif request.data.get('mobile'):
            user = User.objects.filter(mobile=request.data.get('mobile')).values().first()
            if not user['mobile_verified']:
                return Response(responsedata(False, "Mobile not verified"), status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(responsedata(False, "Email id or Mobile is required"), status=status.HTTP_400_BAD_REQUEST)

        if not user["is_active"]:
            return Response(responsedata(False, "Inactive User"), status=status.HTTP_400_BAD_REQUEST)

        if not User.objects.get(uuid=user["uuid"]).check_password(request.data.get("password")):
            return Response(responsedata(False, "Incorrect Password"), status=status.HTTP_400_BAD_REQUEST)

        tokenserializer = TokenObtainPairSerializer(
            data={"uuid": str(user['uuid']), "password": request.data.get("password")})
        if tokenserializer.is_valid(raise_exception=True):
            data = tokenserializer.validate({"uuid": str(user['uuid']), "password": request.data.get("password")})
            data.update(user)
            data.pop("password")
            return Response(responsedata(True, "Sign in successful", data), status=status.HTTP_200_OK)
        else:
            return Response(responsedata(False, "Something went wrong"), status=status.HTTP_400_BAD_REQUEST)


#CRUD of Blog Tag
class BlogTagsList(generics.ListCreateAPIView):
    """List and Create on BlogTags"""
    queryset = BlogTags.objects.all()
    serializer_class = BlogTagsSerializer
    permission_classes = [IsAuthenticated]

class BlogTagsDetail(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update and delete BlogTags"""
    queryset = BlogTags.objects.all()
    serializer_class = BlogTagsSerializer
    permission_classes = [IsAuthenticated]


#CRUD of Blog Categories
class BlogCategoriesDetail(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update and delete BlogCategories"""
    queryset = BlogCategories.objects.all()
    serializer_class = BlogCategoriesSerializer
    permission_classes = [IsAuthenticated]


class BlogCategoriesList(generics.ListCreateAPIView):
    """List and Create on BlogTags"""
    queryset = BlogCategories.objects.all()
    serializer_class = BlogCategoriesSerializer
    permission_classes = [IsAuthenticated]


#CRUD of Blog
class BlogsDetail(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update and delete Blogs"""
    queryset = Blogs.objects.all()
    serializer_class = BlogsSerializer
    permission_classes = [IsAuthenticated]


class BlogsList(generics.ListCreateAPIView):
    """List and Create on Blogs"""
    queryset = Blogs.objects.all()
    serializer_class = BlogsSerializer
    permission_classes = [IsAuthenticated]

#CRUD of BlogComments
class BlogCommentsDetail(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update and delete BlogComments"""
    queryset = BlogComments.objects.all()
    serializer_class = BlogCommentsSerializer
    permission_classes = [IsAuthenticated]


class BlogCommentsList(generics.ListCreateAPIView):
    """List and Create on BlogComments"""
    queryset = BlogComments.objects.all()
    serializer_class = BlogCommentsSerializer
    permission_classes = [IsAuthenticated]

