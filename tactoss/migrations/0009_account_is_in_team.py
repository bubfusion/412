# Generated by Django 4.2.16 on 2024-12-08 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tactoss', '0008_alter_account_join_date_alter_smokegif_published'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='is_in_team',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]