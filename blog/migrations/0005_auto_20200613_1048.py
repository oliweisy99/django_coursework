# Generated by Django 3.0.5 on 2020-06-13 10:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20200612_1156'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blog',
            options={'permissions': (('can_make_changes', 'Can edit, Update or Delete content'),)},
        ),
    ]
