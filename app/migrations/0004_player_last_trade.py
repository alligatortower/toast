# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_player_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='last_trade',
            field=models.CharField(blank=True, null=True, max_length=200),
        ),
    ]
