# Generated by Django 4.1.5 on 2023-07-31 00:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('theatreCheckIn', '0004_remove_movies_original_language_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movies',
            old_name='overview',
            new_name='discription',
        ),
    ]