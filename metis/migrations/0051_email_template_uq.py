# Generated by Django 4.2.12 on 2024-05-08 15:26

from django.db import migrations


class Migration(migrations.Migration):  # noqa: D101
    dependencies = [
        ("metis", "0050_self_evaluations"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="emailtemplate",
            unique_together={("education", "code", "language")},
        ),
    ]