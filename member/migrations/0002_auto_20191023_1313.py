# Generated by Django 2.2.6 on 2019-10-23 13:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='membership',
            unique_together={('member', 'team')},
        ),
    ]
