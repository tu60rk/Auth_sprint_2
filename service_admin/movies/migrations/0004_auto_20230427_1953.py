# Generated by Django 3.2.18 on 2023-04-27 19:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_auto_20221218_1143'),
    ]

    operations = [
        migrations.RenameField(
            model_name='filmwork',
            old_name='genres',
            new_name='all_genres',
        ),
        migrations.RenameField(
            model_name='filmwork',
            old_name='persons',
            new_name='all_persons',
        ),
    ]