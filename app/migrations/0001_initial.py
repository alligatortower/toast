# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
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
                ('gamestate', models.CharField(default='unstarted', choices=[('unstarted', 'Unstarted'), ('choosing', 'Ambassador is Choosing the server'), ('serving', 'The Server is serving drinks'), ('trading', 'Drinks may be traded until the Toast'), ('ended', 'Ended')], max_length=200)),
                ('host', models.BooleanField(default=False)),
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
                ('name', models.CharField(blank=True, null=True, max_length=200)),
                ('session_key', models.CharField(max_length=200)),
                ('alive', models.BooleanField(default=True)),
                ('has_poison', models.BooleanField(default=False)),
                ('server', models.BooleanField(default=False)),
                ('game_owner', models.BooleanField(default=False)),
                ('last_trade', models.CharField(blank=True, null=True, max_length=200)),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='AsymmetricalGame',
            fields=[
                ('game_ptr', models.OneToOneField(parent_link=True, serialize=False, to='app.Game', auto_created=True, primary_key=True)),
                ('winners', models.CharField(blank=True, null=True, choices=[('loyalist', 'Loyalist'), ('traitor', 'Traitor')], max_length=200)),
            ],
            options={
                'abstract': False,
            },
            bases=('app.game',),
        ),
        migrations.CreateModel(
            name='AsymmetricalPlayer',
            fields=[
                ('player_ptr', models.OneToOneField(parent_link=True, serialize=False, to='app.Player', auto_created=True, primary_key=True)),
                ('team', models.CharField(default='unassigned', choices=[('loyalist', 'Loyalist'), ('traitor', 'Traitor'), ('unassigned', 'Unassigned'), ('dead', 'Dead')], max_length=20)),
            ],
            options={
                'abstract': False,
            },
            bases=('app.player',),
        ),
        migrations.CreateModel(
            name='TeamGame',
            fields=[
                ('game_ptr', models.OneToOneField(parent_link=True, serialize=False, to='app.Game', auto_created=True, primary_key=True)),
                ('winners', models.CharField(blank=True, null=True, choices=[('empire', 'Empire'), ('republic', 'Republic')], max_length=200)),
            ],
            options={
                'abstract': False,
            },
            bases=('app.game',),
        ),
        migrations.CreateModel(
            name='TeamPlayer',
            fields=[
                ('player_ptr', models.OneToOneField(parent_link=True, serialize=False, to='app.Player', auto_created=True, primary_key=True)),
                ('team', models.CharField(default='unassigned', choices=[('empire', 'Empire'), ('republic', 'Republic'), ('unassigned', 'Unassigned'), ('dead', 'Dead')], max_length=20)),
            ],
            options={
                'abstract': False,
            },
            bases=('app.player',),
        ),
        migrations.AddField(
            model_name='player',
            name='game',
            field=models.ForeignKey(to='app.Game'),
        ),
        migrations.AddField(
            model_name='player',
            name='polymorphic_ctype',
            field=models.ForeignKey(related_name='polymorphic_app.player_set+', to='contenttypes.ContentType', null=True, editable=False),
        ),
        migrations.AddField(
            model_name='player',
            name='wants_to_trade',
            field=models.ManyToManyField(blank=True, related_name='wants_to_trade_with_me', to='app.Player'),
        ),
        migrations.AddField(
            model_name='game',
            name='polymorphic_ctype',
            field=models.ForeignKey(related_name='polymorphic_app.game_set+', to='contenttypes.ContentType', null=True, editable=False),
        ),
        migrations.AddField(
            model_name='drink',
            name='owner',
            field=models.ForeignKey(to='app.Player'),
        ),
    ]
