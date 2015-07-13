# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asymmetricalplayer',
            name='team',
            field=models.CharField(max_length=20, choices=[('loyalist', 'Loyalist'), ('traitor', 'Traitor')], blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='teamplayer',
            name='team',
            field=models.CharField(max_length=20, choices=[('empire', 'Empire'), ('republic', 'Republic')], blank=True, null=True),
        ),
    ]
