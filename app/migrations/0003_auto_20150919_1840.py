# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20150913_1517'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='list_global_trades',
            field=models.PositiveSmallIntegerField(help_text='leave blank to disable', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='renew_poison_each_round',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='game',
            name='reveal_teams_each_round',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='player',
            name='team_revealed',
            field=models.BooleanField(default=False),
        ),
    ]
