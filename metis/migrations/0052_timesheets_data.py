# Generated by Django 4.2.13 on 2024-06-06 07:41

from django.db import migrations, models


def migrate_existing_data(apps, schema_editor) -> None:
    """Update projects for existing email logs."""
    Absence = apps.get_model("metis", "Absence")
    Timesheet = apps.get_model("metis", "Timesheet")

    models = [Absence, Timesheet]

    for Model in models:
        # bulk save
        updates = []

        for obj in Model.objects.all():
            if obj.comments:
                obj.data["comments"] = obj.comments
                updates.append(obj)

        Model.objects.bulk_update(updates, ["data"])


class Migration(migrations.Migration):  # noqa: D101
    dependencies = [
        ("metis", "0051_email_template_uq"),
    ]

    operations = [
        migrations.AddField(
            model_name="absence",
            name="data",
            field=models.JSONField(default=dict),
        ),
        migrations.AddField(
            model_name="timesheet",
            name="data",
            field=models.JSONField(default=dict),
        ),
        # -----
        migrations.RunPython(migrate_existing_data),
        # -----
        migrations.RemoveField(
            model_name="absence",
            name="comments",
        ),
        migrations.RemoveField(
            model_name="timesheet",
            name="comments",
        ),
    ]
