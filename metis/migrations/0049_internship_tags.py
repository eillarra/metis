# Generated by Django 4.2.11 on 2024-03-18 11:14

from django.db import migrations, models


class Migration(migrations.Migration):  # noqa: D101
    dependencies = [
        ("metis", "0048_place_default_language"),
    ]

    operations = [
        migrations.AddField(
            model_name="internship",
            name="tags",
            field=models.JSONField(default=list),
        ),
    ]
