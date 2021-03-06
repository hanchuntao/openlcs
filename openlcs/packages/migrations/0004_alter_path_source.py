# Generated by Django 3.2 on 2022-02-24 13:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0003_auto_20220224_1322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='path',
            name='source',
            field=models.ForeignKey(help_text='Reference to source package', on_delete=django.db.models.deletion.CASCADE, related_name='file_paths', to='packages.source'),
        ),
    ]
