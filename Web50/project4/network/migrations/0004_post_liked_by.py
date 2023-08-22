# Generated by Django 4.2.2 on 2023-07-12 20:04

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("network", "0003_remove_user_followers_remove_user_following_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="liked_by",
            field=models.ManyToManyField(
                blank=True, related_name="likes", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
