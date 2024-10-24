# Generated by Django 4.2.7 on 2023-11-21 13:00

from django.db import migrations, models


def unencrypt_signed_text(apps, schema_editor) -> None:
    """Unencrypt signed_text from signed_text_encrypted."""
    Signature = apps.get_model("metis", "Signature")

    # bulk save to skip auto_now_add
    updates = []

    for signature in Signature.objects.all():
        signature.signed_text = signature.signed_text_encrypted
        updates.append(signature)

    Signature.objects.bulk_update(updates, ["signed_text"])


class Migration(migrations.Migration):  # noqa: D101
    dependencies = [
        ("metis", "0034_alter_questioning_email_body_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="signature",
            old_name="signed_text",
            new_name="signed_text_encrypted",
        ),
        migrations.AddField(
            model_name="signature",
            name="signed_text",
            field=models.TextField(default=""),
            preserve_default=False,
        ),
        # -----
        migrations.RunPython(unencrypt_signed_text),
        # -----
        migrations.RemoveField(
            model_name="signature",
            name="signed_text_encrypted",
        ),
    ]
