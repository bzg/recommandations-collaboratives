# Generated by Django 3.2.14 on 2022-08-10 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("invites", "0002_auto_20220505_0957"),
    ]

    operations = [
        migrations.AlterField(
            model_name="invite",
            name="role",
            field=models.CharField(
                choices=[
                    ("COLLABORATOR", "Participant·e"),
                    ("SWITCHTENDER", "Conseiller·e"),
                ],
                default="COLLABORATOR",
                max_length=20,
            ),
        ),
    ]
