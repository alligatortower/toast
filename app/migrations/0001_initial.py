# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import model_utils.fields
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Drink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('poisoned', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('created', model_utils.fields.AutoCreatedField(verbose_name='created', editable=False, default=django.utils.timezone.now)),
                ('modified', model_utils.fields.AutoLastModifiedField(verbose_name='modified', editable=False, default=django.utils.timezone.now)),
                ('gamestate', models.CharField(max_length=200, choices=[('unstarted', 'Unstarted'), ('choosing', 'Waiting for Ambassador to choose server'), ('serving', 'Waiting for server to serve drinks'), ('trading', 'Waiting for Ambassador to propose toast'), ('ended', 'Ended')], default='unstarted')),
                ('winners', models.CharField(blank=True, choices=[('loyalist', 'Loyalist'), ('traitor', 'Traitor')], null=True, max_length=200)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('team', models.CharField(max_length=20, choices=[('loyalist', 'Loyalist'), ('traitor', 'Traitor'), ('unassigned', 'Unassigned'), ('ambassador', 'Ambassador'), ('dead', 'Dead')], default='unassigned')),
                ('name', models.CharField(blank=True, null=True, max_length=200)),
                ('session_key', models.CharField(max_length=200)),
                ('alive', models.BooleanField(default=True)),
                ('has_poison', models.BooleanField(default=False)),
                ('server', models.BooleanField(default=False)),
                ('game_owner', models.BooleanField(default=False)),
                ('last_trade', models.CharField(blank=True, null=True, max_length=200)),
                ('game', models.ForeignKey(to='app.Game')),
                ('wants_to_trade', models.ManyToManyField(related_name='wants_to_trade_with_me', blank=True, null=True, to='app.Player')),
            ],
        ),
        migrations.AddField(
            model_name='drink',
            name='owner',
            field=models.ForeignKey(to='app.Player'),
        ),
    ]
