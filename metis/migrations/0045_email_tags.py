# Generated by Django 4.2.10 on 2024-03-11 11:19

from django.db import migrations, models


def update_tags(apps, schema_editor) -> None:
    """Update tags for existing email logs."""
    EmailLog = apps.get_model("metis", "EmailLog")
    User = apps.get_model("metis", "User")

    # bulk save to skip auto_now_add
    updates = []

    for email in EmailLog.objects.all():
        if email.to_user:
            email.tags.append(f"to:{email.to_user.id}")
        else:
            try:
                for e in email.to:
                    user = User.objects.filter(email=e).first()
                    if user:
                        email.tags.append(f"to:{user.id}")
            except AttributeError:
                pass
        updates.append(email)

    EmailLog.objects.bulk_update(updates, ["tags"])


class Migration(migrations.Migration):  # noqa: D101
    dependencies = [
        ("metis", "0044_timesheet_comments"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="emailtemplate",
            name="obj_class",
        ),
        migrations.AddField(
            model_name="emailtemplate",
            name="language",
            field=models.CharField(default="nl", max_length=2),
        ),
        migrations.AddField(
            model_name="emaillog",
            name="tags",
            field=models.JSONField(default=list),
        ),
        # -----
        migrations.RunPython(update_tags),
        # -----
        migrations.RemoveField(
            model_name="emaillog",
            name="to_user",
        ),
    ]