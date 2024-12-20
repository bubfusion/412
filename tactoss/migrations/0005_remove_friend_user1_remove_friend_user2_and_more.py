# Generated by Django 4.2.16 on 2024-11-23 23:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tactoss', '0004_smokegif'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='friend',
            name='user1',
        ),
        migrations.RemoveField(
            model_name='friend',
            name='user2',
        ),
        migrations.RemoveField(
            model_name='smokegif',
            name='user',
        ),
        migrations.RemoveField(
            model_name='team',
            name='user_2',
        ),
        migrations.RemoveField(
            model_name='team',
            name='user_3',
        ),
        migrations.RemoveField(
            model_name='team',
            name='user_4',
        ),
        migrations.RemoveField(
            model_name='team',
            name='user_5',
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_name', models.TextField()),
                ('email', models.EmailField(max_length=254)),
                ('steam_url', models.URLField(blank=True)),
                ('discord_username', models.TextField(blank=True)),
                ('account_picture', models.ImageField(blank=True, upload_to='')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='friend',
            name='account2',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='account2', to='tactoss.account'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='friend',
            name='profiel1',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='account1', to='tactoss.account'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='smokegif',
            name='account',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='tactoss.account'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='team',
            name='account_2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='team_account_2', to='tactoss.account'),
        ),
        migrations.AddField(
            model_name='team',
            name='account_3',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='team_account_3', to='tactoss.account'),
        ),
        migrations.AddField(
            model_name='team',
            name='account_4',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='team_account_4', to='tactoss.account'),
        ),
        migrations.AddField(
            model_name='team',
            name='account_5',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='team_account_5', to='tactoss.account'),
        ),
        migrations.AlterField(
            model_name='team',
            name='team_leader',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tactoss.account'),
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
