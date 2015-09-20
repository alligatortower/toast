# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20150919_2016'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='traderecord',
            options={'ordering': ('-created',)},
        ),
    ]
