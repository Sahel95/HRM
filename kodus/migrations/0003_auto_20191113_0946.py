# Generated by Django 2.2.6 on 2019-11-13 09:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('kodus', '0002_auto_20191023_0842'),
    ]

    operations = [
        migrations.AddField(
            model_name='kudos',
            name='from_member_available_point',
            field=models.IntegerField(default=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='kudos',
            name='to_member_kudos',
            field=models.IntegerField(default=5),
            preserve_default=False,
        ),
    ]
