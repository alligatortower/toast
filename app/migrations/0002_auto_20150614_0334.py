# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='winners',
            field=models.CharField(blank=True, null=True, choices=[('loyalist', 'Loyalist'), ('traitor', 'Traitor')], max_length=200),
        ),
        migrations.AlterField(
            model_name='player',
            name='team',
            field=models.CharField(max_length=20, choices=[('loyalist', 'Loyalist'), ('traitor', 'Traitor'), ('unassigned', 'Unassigned'), ('ambassador', 'Ambassador'), ('dead', 'Dead')], default='unassigned'),
        ),
    ]
