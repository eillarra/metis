# Generated by Django 4.2.6 on 2023-10-12 19:36

from django.db import migrations, models


class Migration(migrations.Migration):  # noqa: D101
    dependencies = [
        ("metis", "0027_internship_dates"),
    ]

    operations = [
        migrations.AddField(
            model_name="student",
            name="number",
            field=models.CharField(blank=True, max_length=8, null=True),
        ),
    ]
