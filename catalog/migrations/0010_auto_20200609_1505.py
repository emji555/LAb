# Generated by Django 3.0.5 on 2020-06-09 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0009_author_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='image',
            field=models.ImageField(upload_to='catalog-image'),
        ),
    ]
