# Generated by Django 5.1.1 on 2024-10-16 10:38

from django.db import migrations, models

import metis.models.validators


class Migration(migrations.Migration):  # noqa: D101
    dependencies = [
        ("metis", "0057_questioning_disable_emails"),
    ]

    operations = [
        migrations.AddField(
            model_name="place",
            name="tags",
            field=models.JSONField(default=list, validators=[metis.models.validators.validate_list_of_strings]),
        ),
        migrations.AlterField(
            model_name="internship",
            name="tags",
            field=models.JSONField(default=list, validators=[metis.models.validators.validate_list_of_strings]),
        ),
    ]
