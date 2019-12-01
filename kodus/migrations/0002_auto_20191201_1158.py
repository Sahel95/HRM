# Generated by Django 2.2.6 on 2019-12-01 11:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('kodus', '0001_initial'),
        ('member', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='kudos',
            name='from_member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='kudosfrom', to='member.Members'),
        ),
        migrations.AddField(
            model_name='kudos',
            name='to_member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='kudosto', to='member.Members'),
        ),
    ]