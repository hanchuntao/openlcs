# Generated by Django 3.2 on 2022-03-21 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0005_alter_package_source'),
    ]

    operations = [
        migrations.AddField(
            model_name='source',
            name='scan_flag',
            field=models.TextField(blank=True, help_text='A comma separated "scan_type(detector)"', null=True),
        ),
    ]
