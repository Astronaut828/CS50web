# Generated by Django 4.2.2 on 2023-06-26 15:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0003_rename_listings_listing"),
    ]

    operations = [
        migrations.AlterField(
            model_name="listing",
            name="created_time",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]