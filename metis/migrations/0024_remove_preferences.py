# Generated by Django 4.2.5 on 2023-10-04 8:24

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("metis", "0023_mentors"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="placepreference",
            name="place",
        ),
        migrations.RemoveField(
            model_name="placepreference",
            name="preference",
        ),
        migrations.RemoveField(
            model_name="preference",
            name="created_by",
        ),
        migrations.RemoveField(
            model_name="preference",
            name="disciplines",
        ),
        migrations.RemoveField(
            model_name="preference",
            name="internship",
        ),
        migrations.RemoveField(
            model_name="preference",
            name="places",
        ),
        migrations.RemoveField(
            model_name="preference",
            name="student",
        ),
        migrations.RemoveField(
            model_name="preference",
            name="updated_by",
        ),
        migrations.DeleteModel(
            name="DisciplinePreference",
        ),
        migrations.DeleteModel(
            name="PlacePreference",
        ),
        migrations.DeleteModel(
            name="Preference",
        ),
    ]