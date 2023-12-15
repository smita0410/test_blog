import uuid
import datetime

from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from .managers import UserManager
from django.contrib.postgres.fields import ArrayField


# Create your models here.

class BaseModel(models.Model):
    class Meta:
        abstract = True

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_seconds_since_creation(self):
        return (datetime.datetime.utcnow() - self.created_at.replace(tzinfo=None)).seconds


class User(BaseModel, AbstractBaseUser, PermissionsMixin):

    name = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=100, unique=True, null=True)
    email_verified = models.BooleanField(default=False)
    mobile = models.BigIntegerField(null=True)
    mobile_verified = models.BooleanField(default=False)
    password = models.CharField(max_length=100, null=True)
    profile_image = models.TextField(null=True) #Considering s3 url for profile image
    bio = models.TextField(null=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'uuid'

    class Meta:
        db_table = 'User'


class BlogTags(BaseModel):

    tag = models.CharField(max_length=255)
    description = models.TextField(null=True)

    class Meta:
        db_table = 'BlogTags'

class BlogCategories(BaseModel):

    category = models.CharField(max_length=255)
    description = models.TextField(null=True)

    class Meta:
        db_table = 'BlogCategories'


class Blogs(BaseModel):

    title = models.CharField(max_length=255)
    content = models.TextField(null=True)
    published_on = models.DateTimeField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(BlogTags)
    categories = models.ManyToManyField(BlogCategories)

    class Meta:
        db_table = 'Blogs'


class BlogComments(BaseModel):
    comments = models.TextField(null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    blogs = models.ForeignKey(Blogs, on_delete=models.CASCADE)

    class Meta:
        db_table = 'BlogComments'

