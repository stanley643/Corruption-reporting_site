# Generated by Django 5.0.3 on 2024-04-02 05:56

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0005_auto_20240305_0000'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='chat_room',
        ),
        migrations.RemoveField(
            model_name='message',
            name='content',
        ),
        migrations.RemoveField(
            model_name='message',
            name='created_at',
        ),
        migrations.AddField(
            model_name='message',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='message',
            name='room',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to='report.chatroom'),
        ),
        migrations.AddField(
            model_name='message',
            name='value',
            field=models.CharField(default='', max_length=1000000),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='message',
            name='user',
            field=models.CharField(max_length=100),
        ),
    ]
