# Generated by Django 4.2.13 on 2024-07-16 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0100_remove_projectsite_unique_origin_site_and_more"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="projectsite",
            constraint=models.UniqueConstraint(
                fields=("project", "site"), name="unique_site_per_project"
            ),
        ),
    ]
