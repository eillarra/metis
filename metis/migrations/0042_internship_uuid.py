# Generated by Django 4.2.9 on 2024-01-24 14:39

import uuid

from django.db import migrations, models


def generate_uuids(apps, schema_editor):
    """Generate UUIDs for existing internships."""
    Internship = apps.get_model("metis", "Internship")

    # bulk save to skip auto_now_add
    updates = []

    for internship in Internship.objects.all():
        internship.uuid = uuid.uuid4()
        updates.append(internship)

    Internship.objects.bulk_update(updates, ["uuid"])


class Migration(migrations.Migration):
    dependencies = [
        ("metis", "0041_alter_internship_project_place"),
    ]

    operations = [
        migrations.AddField(
            model_name="internship",
            name="uuid",
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        # -----
        migrations.RunPython(generate_uuids),
        # -----
        migrations.AlterField(
            model_name="internship",
            name="uuid",
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]