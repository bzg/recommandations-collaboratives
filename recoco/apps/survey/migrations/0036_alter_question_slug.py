# Generated by Django 4.2.13 on 2024-06-17 10:25

import autoslug.fields
from django.db import migrations
import recoco.apps.survey.models


class Migration(migrations.Migration):

    dependencies = [
        ("survey", "0035_fill_question_slugs"),
    ]

    operations = [
        migrations.AlterField(
            model_name="question",
            name="slug",
            field=autoslug.fields.AutoSlugField(
                editable=False,
                populate_from=recoco.apps.survey.models.Question._populate_slug,
                unique=True,
            ),
        ),
    ]
