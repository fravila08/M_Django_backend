# Generated by Django 4.2.2 on 2023-07-10 13:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts_app', '0002_comment_replies_post_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='date_created',
            field=models.DateField(default=datetime.date(2023, 7, 10)),
        ),
    ]