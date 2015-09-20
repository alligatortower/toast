# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20150919_2019'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='trades_this_round',
        ),
    ]
