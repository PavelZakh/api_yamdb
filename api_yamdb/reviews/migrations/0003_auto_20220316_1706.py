# Generated by Django 2.2.16 on 2022-03-16 12:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20220316_1642'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comments',
            old_name='review_id',
            new_name='review',
        ),
        migrations.RenameField(
            model_name='comments',
            old_name='title_id',
            new_name='title',
        ),
        migrations.RenameField(
            model_name='reviews',
            old_name='title_id',
            new_name='title',
        ),
    ]