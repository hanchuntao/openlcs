# Generated by Django 3.2 on 2022-03-11 01:29

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('packages', '0005_alter_package_source'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileLicenseScan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detector', models.CharField(help_text='License detector with version detail', max_length=32)),
                ('file', models.ForeignKey(help_text='Reference to a file', on_delete=django.db.models.deletion.CASCADE, related_name='license_scans', to='packages.file')),
            ],
        ),
        migrations.CreateModel(
            name='LicenseDetection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('license_key', models.CharField(max_length=128, verbose_name='license identifier')),
                ('score', models.FloatField(blank=True, help_text='License match score (0 - 100)', null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('rule', models.TextField(blank=True, help_text='How the license is detected', null=True)),
                ('start_line', models.IntegerField(blank=True, help_text='Beginning of license match', null=True)),
                ('end_line', models.IntegerField(blank=True, help_text='End of license match', null=True)),
                ('false_positive', models.BooleanField(default=False, help_text='True if this detection is a false positive')),
                ('file_scan', models.ForeignKey(help_text='Reference to a file license scan', on_delete=django.db.models.deletion.CASCADE, related_name='license_detections', to='reports.filelicensescan')),
            ],
        ),
        migrations.CreateModel(
            name='FileCopyrightScan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detector', models.CharField(help_text='Copyright detector with version detail', max_length=32)),
                ('file', models.ForeignKey(help_text='Reference to a file', on_delete=django.db.models.deletion.CASCADE, related_name='copyright_scans', to='packages.file')),
            ],
        ),
        migrations.CreateModel(
            name='CopyrightDetection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('statement', models.TextField(help_text='Copyright statement')),
                ('false_positive', models.BooleanField(default=False, help_text='True if this detection is a false positive')),
                ('start_line', models.IntegerField(blank=True, help_text='Beginning of copyright match', null=True)),
                ('end_line', models.IntegerField(blank=True, help_text='End of copyright match', null=True)),
                ('file_scan', models.ForeignKey(help_text='Reference to a file copyright scan', on_delete=django.db.models.deletion.CASCADE, related_name='copyright_detections', to='reports.filecopyrightscan')),
            ],
        ),
    ]
