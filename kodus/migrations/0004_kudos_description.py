# Generated by Django 2.2.6 on 2019-11-19 08:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('kodus', '0003_auto_20191113_0946'),
    ]

    operations = [
        migrations.AddField(
            model_name='kudos',
            name='description',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
