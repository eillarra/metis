# Generated by Django 4.2.6 on 2023-10-24 08:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("metis", "0030_delete_invitation"),
    ]

    operations = [
        migrations.CreateModel(
            name="EvaluationForm",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("form_definition", models.JSONField(default=dict)),
                ("email_subject", models.CharField(max_length=255)),
                ("email_body", models.TextField()),
                ("email_add_office_in_bcc", models.BooleanField(default=False)),
                ("version", models.PositiveSmallIntegerField(default=1)),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_created_by",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "discipline",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="evaluation_forms",
                        to="metis.discipline",
                    ),
                ),
                (
                    "period",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="evaluation_forms",
                        to="metis.period",
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="evaluation_forms", to="metis.project"
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_updated_by",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "metis_project_evaluation_forms",
                "ordering": ["project", "-version"],
                "unique_together": {("project", "period", "discipline", "version")},
            },
        ),
        migrations.CreateModel(
            name="Evaluation",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("data", models.JSONField(default=dict)),
                ("intermediate", models.PositiveSmallIntegerField(default=0)),
                ("is_approved", models.BooleanField(default=False)),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_created_by",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "form",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="evaluations",
                        to="metis.evaluationform",
                    ),
                ),
                (
                    "internship",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="evaluations", to="metis.internship"
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_updated_by",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "metis_internship_evaluation",
                "unique_together": {("internship", "intermediate")},
            },
        ),
    ]