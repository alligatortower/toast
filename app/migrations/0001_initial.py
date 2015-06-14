# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Drink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('poisoned', models.BooleanField(default=False)),
                ('icon', models.CharField(default='/static/img/drink-icons/beer-bottle.png', choices=[('/static/img/drink-icons/beer-bottle.png', 'Beer Bottle'), ('/static/img/drink-icons/can.png', 'Beer Can'), ('/static/img/drink-icons/champagne.png', 'Champagne'), ('/static/img/drink-icons/cocktail.png', 'Cocktail'), ('/static/img/drink-icons/coffee.png', 'Coffee'), ('/static/img/drink-icons/milk.png', 'Milk'), ('/static/img/drink-icons/on-rocks.png', 'On the Rocks'), ('/static/img/drink-icons/orange-slice.png', 'Old Fashioned'), ('/static/img/drink-icons/pint.png', 'Pint'), ('/static/img/drink-icons/tropical.png', 'Tropical'), ('/static/img/drink-icons/wedge-on-rim.png', 'With a wedge'), ('/static/img/drink-icons/wine.png', 'Wine')], max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('gamestate', models.CharField(default='unstarted', choices=[('unstarted', 'Unstarted'), ('choosing', 'Waiting for Ambassador to choose server'), ('serving', 'Waiting for server to serve drinks'), ('trading', 'Waiting for Ambassador to propose toast'), ('ended', 'Ended')], max_length=200)),
                ('winners', models.CharField(null=True, choices=[('loyalist', 'Loyalist'), ('traitor', 'Traitor')], max_length=200, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('team', models.CharField(default='unassigned', choices=[('loyalist', 'Loyalist'), ('traitor', 'Traitor'), ('unassigned', 'Unassigned'), ('ambassador', 'Ambassador'), ('dead', 'Dead')], max_length=20)),
                ('name', models.CharField(null=True, max_length=200, blank=True)),
                ('session_key', models.CharField(max_length=200)),
                ('alive', models.BooleanField(default=True)),
                ('has_poison', models.BooleanField(default=False)),
                ('server', models.BooleanField(default=False)),
                ('game_owner', models.BooleanField(default=False)),
                ('last_trade', models.CharField(null=True, max_length=200, blank=True)),
                ('game', models.ForeignKey(to='app.Game')),
                ('wants_to_trade', models.ManyToManyField(to='app.Player', null=True, related_name='wants_to_trade_with_me', blank=True)),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.AddField(
            model_name='drink',
            name='owner',
            field=models.ForeignKey(to='app.Player'),
        ),
    ]
