# Generated by Django 5.0.1 on 2024-03-03 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('muscleforge', '0006_alter_goal_status_delete_progresstracker'),
    ]

    operations = [
        migrations.AddField(
            model_name='goal',
            name='title',
            field=models.TextField(blank=True, null=True),
        ),
    ]
