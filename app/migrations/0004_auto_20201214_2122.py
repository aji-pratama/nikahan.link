# Generated by Django 3.1.3 on 2020-12-14 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20201130_0857'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wedding',
            name='time',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
    ]