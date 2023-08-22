# Generated by Django 4.2.2 on 2023-06-22 23:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Listings",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("listing_title", models.CharField(default="", max_length=255)),
                ("listing_description", models.TextField(default="")),
                ("listing_pic", models.URLField(default="")),
                ("category", models.CharField(default="Uncategorized", max_length=255)),
                (
                    "starting_bid",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                ("is_active", models.BooleanField(default=True)),
                (
                    "created_time",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]