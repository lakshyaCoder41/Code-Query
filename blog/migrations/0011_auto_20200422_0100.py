# Generated by Django 3.0.4 on 2020-04-22 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='image',
            field=models.ImageField(null=True, upload_to='comment_pics'),
        ),
    ]