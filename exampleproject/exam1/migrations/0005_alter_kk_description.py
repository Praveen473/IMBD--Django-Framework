# Generated by Django 4.2.6 on 2023-12-15 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam1', '0004_kk_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kk',
            name='description',
            field=models.CharField(max_length=10),
        ),
    ]