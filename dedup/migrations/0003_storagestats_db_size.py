# Generated by Django 5.1.4 on 2024-12-30 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dedup', '0002_storagestats'),
    ]

    operations = [
        migrations.AddField(
            model_name='storagestats',
            name='db_size',
            field=models.BigIntegerField(default=0),
        ),
    ]