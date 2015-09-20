# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_remove_game_trades_this_round'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='asymmetricalgame',
            name='winners',
        ),
        migrations.RemoveField(
            model_name='teamgame',
            name='winners',
        ),
        migrations.AddField(
            model_name='game',
            name='host_can_force_trades',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='game',
            name='no_kill_rounds_before_draw',
            field=models.PositiveSmallIntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='game',
            name='rounds_without_kill',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='game',
            name='winners',
            field=models.CharField(null=True, max_length=200, blank=True),
        ),
    ]
