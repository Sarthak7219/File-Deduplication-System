# Generated by Django 5.1.4 on 2024-12-30 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dedup', '0004_filerecord'),
    ]

    operations = [
        migrations.RenameField(
            model_name='storagestats',
            old_name='db_size',
            new_name='total_dedup_size',
        ),
        migrations.RemoveField(
            model_name='filerecord',
            name='hash_file_path',
        ),
        migrations.RemoveField(
            model_name='storagestats',
            name='media_folder_size',
        ),
        migrations.AddField(
            model_name='filerecord',
            name='hash_string',
            field=models.TextField(blank=True, null=True),
        ),
    ]