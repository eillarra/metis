# Generated by Django 4.2.7 on 2023-11-29 11:44

from django.db import migrations

from metis.services.form_builder.evaluations import (
    validate_evaluation_form_definition,
    validate_evaluation_form_response,
)
from metis.utils.fixtures.forms.evaluations import get_audio_internship_evaluation_form_klinisch


def map_score(score: int | float) -> str:
    """Map score to a string."""
    return {
        None: None,
        1.0: "onv",
        2.0: "onv/nv",
        3.0: "nv",
        4.0: "nv/vol",
        5.0: "vol",
        5.5: "vol/g",
        6.0: "g",
        7.0: "g/zg",
        8.0: "zg",
        8.5: "zg/u",
        9.0: "u",
    }[float(score) if score is not None else None]


def refactor_form_definitions(apps, schema_editor):
    """Refactor form definitions to use a new format."""
    EvaluationForm = apps.get_model("metis", "EvaluationForm")
    example_form = get_audio_internship_evaluation_form_klinisch()

    # bulk save to skip auto_now_add
    updates = []

    for evaluation_form in EvaluationForm.objects.all():
        """Changes:
        - remove `global_evaluation` and `global_section_evaluation`
        - per section, rename `add_remarks` to `with_remarks`
        """
        form_definition = evaluation_form.form_definition
        form_definition["scores"] = example_form["scores"]
        form_definition.pop("grades", None)
        form_definition.pop("global_evaluation", None)
        form_definition.pop("global_section_evaluation", None)
        for section in form_definition["sections"]:
            if "add_remarks" in section:
                section["with_remarks"] = section.pop("add_remarks")
        evaluation_form.form_definition = form_definition
        validate_evaluation_form_definition(form_definition)
        updates.append(evaluation_form)

    EvaluationForm.objects.bulk_update(updates, ["form_definition"])


def refactor_evaluation_responses(apps, schema_editor):
    """Refactor evaluation responses to use a new format."""
    Evaluation = apps.get_model("metis", "Evaluation")

    # bulk save to skip auto_now_add
    updates = []

    for evaluation in Evaluation.objects.all():
        """Changes:
        - update scores, using value instead of points
        """
        evaluation_data = evaluation.data
        evaluation_data["global_remarks"] = evaluation_data.pop("remarks__final", "")
        evaluation_data["global_score"] = map_score(evaluation_data.pop("grade__final", None))
        evaluation_data["sections"] = {}

        for section in evaluation.form.form_definition["sections"]:
            section_data = evaluation_data[section["code"]]
            section_data["score"] = map_score(section_data.pop("grade"))
            section_data["scores"] = section_data.pop("grades")

            if section["with_remarks"]:
                section_data["remarks"] = section_data.pop("remarks", None) or ""

            for key, value in section_data["scores"].items():
                section_data["scores"][key] = (map_score(value[0]), value[1])

            evaluation_data["sections"][section["code"]] = section_data
            del evaluation_data[section["code"]]

        evaluation.data = evaluation_data
        validate_evaluation_form_response(evaluation.form.form_definition, evaluation_data)
        updates.append(evaluation)

    Evaluation.objects.bulk_update(updates, ["data"])


class Migration(migrations.Migration):
    """Refactor evaluations."""

    dependencies = [
        ("metis", "0036_alter_evaluation_options"),
    ]

    operations = [
        # -----
        migrations.RunPython(refactor_form_definitions),
        migrations.RunPython(refactor_evaluation_responses),
        # -----
    ]
