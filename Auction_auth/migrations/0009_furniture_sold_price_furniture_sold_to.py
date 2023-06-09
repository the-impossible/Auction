# Generated by Django 4.2 on 2023-05-01 03:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("Auction_auth", "0008_bidding"),
    ]

    operations = [
        migrations.AddField(
            model_name="furniture",
            name="sold_price",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="furniture",
            name="sold_to",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
