# Generated by Django 4.2.16 on 2024-12-09 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tactoss', '0015_alter_account_account_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='account_picture',
            field=models.ImageField(blank=True, default='default.jpg', upload_to=''),
        ),
        migrations.DeleteModel(
            name='Friend',
        ),
    ]
