# Generated by Django 5.2 on 2025-05-06 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_category_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image_url',
            field=models.URLField(blank=True, max_length=1024, null=True),
        ),
    ]
