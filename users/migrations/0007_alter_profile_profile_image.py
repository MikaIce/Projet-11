# Generated by Django 4.1.2 on 2023-06-06 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_profile_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(default='default_male.jpg', upload_to='profile_images/'),
        ),
    ]
