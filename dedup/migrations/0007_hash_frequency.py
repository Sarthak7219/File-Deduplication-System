# Generated by Django 5.1.4 on 2024-12-30 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dedup', '0006_rename_total_dedup_size_storagestats_total_hash_size_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='hash',
            name='frequency',
            field=models.IntegerField(default=0),
        ),
    ]