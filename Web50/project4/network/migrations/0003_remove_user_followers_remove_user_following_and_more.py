# Generated by Django 4.2.2 on 2023-07-06 21:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("network", "0002_user_followers_user_following_alter_user_id_post"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="followers",
        ),
        migrations.RemoveField(
            model_name="user",
            name="following",
        ),
        migrations.AlterField(
            model_name="post",
            name="timestamp",
            field=models.DateTimeField(),
        ),
        migrations.CreateModel(
            name="Following",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                (
                    "following_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="followers",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="following",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
