# Generated by Django 4.1.5 on 2023-07-31 00:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('theatreCheckIn', '0003_alter_movies_original_language'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movies',
            name='original_language',
        ),
        migrations.RemoveField(
            model_name='movies',
            name='original_title',
        ),
        migrations.RemoveField(
            model_name='movies',
            name='poster_path',
        ),
    ]