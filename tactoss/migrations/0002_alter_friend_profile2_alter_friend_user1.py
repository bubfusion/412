# Generated by Django 4.2.16 on 2024-11-22 18:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tactoss', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friend',
            name='profile2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user2', to='tactoss.user'),
        ),
        migrations.AlterField(
            model_name='friend',
            name='user1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user1', to='tactoss.user'),
        ),
    ]
