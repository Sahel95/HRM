# Generated by Django 2.2.6 on 2019-10-20 10:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0003_members_score'),
    ]

    operations = [
        migrations.RenameField(
            model_name='members',
            old_name='score',
            new_name='point',
        ),
    ]
