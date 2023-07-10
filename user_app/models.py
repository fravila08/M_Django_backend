from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class App_User(AbstractUser):
    preferred_name = models.CharField(max_length=30, default="Unknown")
    email = models.EmailField(unique=True)
    USERNAME_FIELD= "email"
    REQUIRED_FIELDS = []
    friends = models.ManyToManyField("App_User")
