# Generated by Django 3.2 on 2022-01-05 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='source',
            name='checksum',
            field=models.CharField(help_text='Checksum for this package', max_length=64, unique=True),
        ),
    ]