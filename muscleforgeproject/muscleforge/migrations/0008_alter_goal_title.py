# Generated by Django 5.0.1 on 2024-03-03 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('muscleforge', '0007_goal_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goal',
            name='title',
            field=models.TextField(blank=True, max_length=100, null=True),
        ),
    ]