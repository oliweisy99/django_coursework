# Generated by Django 3.0.5 on 2020-06-12 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_blog_blog_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='blog_pic',
            field=models.ImageField(blank=True, upload_to='media/'),
        ),
    ]
