# Generated by Django 3.0.4 on 2020-04-20 00:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20200419_2317'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='user',
            new_name='name',
        ),
    ]
