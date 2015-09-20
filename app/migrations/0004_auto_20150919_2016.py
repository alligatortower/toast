# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import model_utils.fields
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20150919_1840'),
    ]

    operations = [
        migrations.CreateModel(
            name='TradeRecord',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('created', model_utils.fields.AutoCreatedField(editable=False, default=django.utils.timezone.now, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(editable=False, default=django.utils.timezone.now, verbose_name='modified')),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.AddField(
            model_name='game',
            name='minimum_trades_per_round',
            field=models.PositiveSmallIntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='game',
            name='trades_this_round',
            field=models.PositiveSmallIntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='traderecord',
            name='game',
            field=models.ForeignKey(to='app.Game'),
        ),
        migrations.AddField(
            model_name='traderecord',
            name='offerer',
            field=models.ForeignKey(related_name='offerer', to='app.Player'),
        ),
        migrations.AddField(
            model_name='traderecord',
            name='receiver',
            field=models.ForeignKey(related_name='receiver', to='app.Player'),
        ),
    ]
