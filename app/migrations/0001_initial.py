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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('poisoned', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(verbose_name='created', default=django.utils.timezone.now, editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(verbose_name='modified', default=django.utils.timezone.now, editable=False)),
                ('gamestate', models.CharField(default='unstarted', choices=[('unstarted', 'Unstarted'), ('choosing', 'Waiting for Ambassador to choose server'), ('serving', 'Waiting for server to serve drinks'), ('trading', 'Waiting for Ambassador to propose toast'), ('ended', 'Ended')], max_length=200)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('team', models.CharField(default='unassigned', choices=[('unassigned', 'Unassigned'), ('ambassador', 'Ambassador'), ('loyalist', 'Loyalist'), ('traitor', 'Traitor'), ('dead', 'Dead')], max_length=20)),
                ('session_key', models.CharField(max_length=200)),
                ('alive', models.BooleanField(default=True)),
                ('has_poison', models.BooleanField(default=False)),
                ('server', models.BooleanField(default=False)),
                ('game_owner', models.BooleanField(default=False)),
                ('game', models.ForeignKey(to='app.Game')),
                ('wants_to_trade', models.ManyToManyField(null=True, related_name='wants_to_trade_with_me', blank=True, to='app.Player')),
            ],
        ),
        migrations.AddField(
            model_name='drink',
            name='owner',
            field=models.ForeignKey(to='app.Player'),
        ),
    ]
