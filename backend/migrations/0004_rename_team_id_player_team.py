# Generated by Django 5.0.4 on 2024-04-11 16:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_alter_match_tournament'),
    ]

    operations = [
        migrations.RenameField(
            model_name='player',
            old_name='team_id',
            new_name='team',
        ),
    ]
