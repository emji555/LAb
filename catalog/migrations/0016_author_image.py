# Generated by Django 3.0.5 on 2020-06-09 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0015_remove_author_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='catalog-image'),
        ),
    ]