# Generated by Django 2.1.5 on 2019-02-03 04:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='managedfile',
            unique_together={('dir', 'name')},
        ),
    ]
