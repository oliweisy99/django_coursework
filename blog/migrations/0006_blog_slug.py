# Generated by Django 3.0.5 on 2020-06-13 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20200613_1048'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='slug',
            field=models.SlugField(allow_unicode=True, null=True, unique=True),
        ),
    ]
