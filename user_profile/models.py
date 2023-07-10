from django.db import models
from user_app.models import App_User
from django.core import validators as v

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(App_User, on_delete=models.CASCADE)
    years_of_xp = models.PositiveIntegerField(default=0, validators=[v.MaxValueValidator(40)])
    job_title = models.CharField(default="NONE",max_length=100, validators=[v.MinLengthValidator(1)])
    profession = models.CharField(default="NONE",max_length=100, validators=[v.MinLengthValidator(1)])
    employer = models.CharField(default="NONE",max_length=100, validators=[v.MinLengthValidator(1)])
    bio = models.TextField(default="NONE",validators=[v.MaxValueValidator(500)])
