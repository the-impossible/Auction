# Generated by Django 4.2 on 2023-04-27 16:05

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("Auction_auth", "0002_alter_user_picture"),
    ]

    operations = [
        migrations.CreateModel(
            name="Furniture",
            fields=[
                (
                    "furniture_id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("furniture_name", models.CharField(max_length=100)),
                ("start_price", models.FloatField()),
                ("furniture_desc", models.TextField()),
                (
                    "created",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="date_created"
                    ),
                ),
                ("start_date_and_time", models.DateTimeField()),
                ("end_date_and_time", models.DateTimeField()),
                (
                    "image",
                    models.ImageField(blank=True, null=True, upload_to="uploads/"),
                ),
            ],
            options={"verbose_name_plural": "Furniture", "db_table": "Furniture",},
        ),
    ]
