# Generated by Django 4.2.1 on 2023-05-26 13:22

from django.db import migrations


class Migration(migrations.Migration):  # noqa: D101
    dependencies = [
        ("metis", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="tmpmentor",
            name="place",
        ),
        migrations.RemoveField(
            model_name="tmpmentor",
            name="project",
        ),
        migrations.RemoveField(
            model_name="tmpplacedata",
            name="discipline",
        ),
        migrations.RemoveField(
            model_name="tmpplacedata",
            name="place",
        ),
        migrations.RemoveField(
            model_name="tmpstudent",
            name="block",
        ),
        migrations.RemoveField(
            model_name="tmpstudent",
            name="project",
        ),
        migrations.DeleteModel(
            name="TmpInternship",
        ),
        migrations.DeleteModel(
            name="TmpMentor",
        ),
        migrations.DeleteModel(
            name="TmpPlaceData",
        ),
        migrations.DeleteModel(
            name="TmpStudent",
        ),
    ]
