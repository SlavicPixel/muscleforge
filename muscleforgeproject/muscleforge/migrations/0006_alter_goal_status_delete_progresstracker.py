# Generated by Django 5.0.1 on 2024-03-03 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('muscleforge', '0005_exercise_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goal',
            name='status',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='ProgressTracker',
        ),
    ]