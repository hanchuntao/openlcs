# Generated by Django 3.2 on 2021-11-29 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='swhid',
            field=models.CharField(help_text='SoftWare Heritage persistent IDentifier', max_length=50, unique=True, verbose_name='SWH ID'),
        ),
    ]
