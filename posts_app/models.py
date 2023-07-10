from django.db import models
from user_app.models import App_User
from django.core import validators as v
from django.utils.timezone import now

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(App_User, on_delete=models.CASCADE)
    likes = models.PositiveIntegerField(default=0)
    content = models.TextField(validators=[v.MinLengthValidator(1)])
    comments = models.PositiveIntegerField(default=0)
    date_created = models.DateTimeField(default=now())

    def liked(self):
        self.likes += 1

    def unliked(self):
        self.likes -= 1

class Comment(models.Model):
    user = models.ForeignKey(App_User, on_delete=models.CASCADE)
    parent_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    likes = models.PositiveIntegerField(default=0)
    content = models.TextField(validators=[v.MinLengthValidator(1)])
    replies = models.PositiveIntegerField(default=0)

    def liked(self):
        self.likes += 1

    def unliked(self):
        self.likes -= 1

class Reply(models.Model):
    user = models.ForeignKey(App_User, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    likes = models.PositiveIntegerField(default=0)
    content = models.TextField(validators=[v.MinLengthValidator(1)])

    def liked(self):
        self.likes += 1

    def unliked(self):
        self.likes -= 1