# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='player',
            options={'ordering': ('created',), 'get_latest_by': 'created'},
        ),
        migrations.AlterField(
            model_name='game',
            name='gamestate',
            field=models.CharField(choices=[('unstarted', 'Unstarted'), ('choosing', 'The Host is Choosing the Server'), ('serving', 'The Server is serving drinks'), ('trading', 'Drinks may be traded until the Toast'), ('toast_proposed', 'All drinks must be raised to toast'), ('toast', 'All drinks must be raised to toast'), ('ended', 'Ended')], max_length=200, default='unstarted'),
        ),
    ]
