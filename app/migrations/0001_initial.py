# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import model_utils.fields
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Drink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('poisoned', models.BooleanField(default=False)),
                ('icon', models.CharField(default='/static/img/drink-icons/beer-bottle.png', choices=[('/static/img/drink-icons/beer-bottle.png', 'Beer Bottle'), ('/static/img/drink-icons/can.png', 'Beer Can'), ('/static/img/drink-icons/champagne.png', 'Champagne'), ('/static/img/drink-icons/cocktail.png', 'Cocktail'), ('/static/img/drink-icons/coffee.png', 'Coffee'), ('/static/img/drink-icons/milk.png', 'Milk'), ('/static/img/drink-icons/on-rocks.png', 'On the Rocks'), ('/static/img/drink-icons/orange-slice.png', 'Old Fashioned'), ('/static/img/drink-icons/pint.png', 'Pint'), ('/static/img/drink-icons/tropical.png', 'Tropical'), ('/static/img/drink-icons/wedge-on-rim.png', 'With a wedge'), ('/static/img/drink-icons/wine.png', 'Wine')], max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('gamestate', models.CharField(default='unstarted', choices=[('unstarted', 'Unstarted'), ('choosing', 'Ambassador is Choosing the server'), ('serving', 'The Server is serving drinks'), ('trading', 'Drinks may be traded until the Toast'), ('toast_proposed', 'All drinks must be raised to toast'), ('toast', 'All drinks must be raised to toast'), ('ended', 'Ended')], max_length=200)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('host', models.BooleanField(default=False)),
                ('name', models.CharField(null=True, blank=True, max_length=200)),
                ('session_key', models.CharField(max_length=200)),
                ('alive', models.BooleanField(default=True)),
                ('has_poison', models.BooleanField(default=False)),
                ('server', models.BooleanField(default=False)),
                ('drink_raised', models.BooleanField(default=False)),
                ('game_owner', models.BooleanField(default=False)),
                ('last_trade', models.CharField(null=True, blank=True, max_length=200)),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='AsymmetricalGame',
            fields=[
                ('game_ptr', models.OneToOneField(auto_created=True, primary_key=True, to='app.Game', serialize=False, parent_link=True)),
                ('winners', models.CharField(choices=[('loyalist', 'Loyalist'), ('traitor', 'Traitor')], null=True, blank=True, max_length=200)),
            ],
            options={
                'abstract': False,
            },
            bases=('app.game',),
        ),
        migrations.CreateModel(
            name='AsymmetricalPlayer',
            fields=[
                ('player_ptr', models.OneToOneField(auto_created=True, primary_key=True, to='app.Player', serialize=False, parent_link=True)),
                ('team', models.CharField(choices=[('loyalist', 'Loyalist'), ('traitor', 'Traitor')], null=True, blank=True, max_length=20)),
            ],
            options={
                'abstract': False,
            },
            bases=('app.player',),
        ),
        migrations.CreateModel(
            name='TeamGame',
            fields=[
                ('game_ptr', models.OneToOneField(auto_created=True, primary_key=True, to='app.Game', serialize=False, parent_link=True)),
                ('winners', models.CharField(choices=[('empire', 'Empire'), ('republic', 'Republic')], null=True, blank=True, max_length=200)),
            ],
            options={
                'abstract': False,
            },
            bases=('app.game',),
        ),
        migrations.CreateModel(
            name='TeamPlayer',
            fields=[
                ('player_ptr', models.OneToOneField(auto_created=True, primary_key=True, to='app.Player', serialize=False, parent_link=True)),
                ('team', models.CharField(choices=[('empire', 'Empire'), ('republic', 'Republic')], null=True, blank=True, max_length=20)),
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
            field=models.ForeignKey(to='contenttypes.ContentType', null=True, related_name='polymorphic_app.player_set+', editable=False),
        ),
        migrations.AddField(
            model_name='player',
            name='wants_to_trade',
            field=models.ManyToManyField(related_name='wants_to_trade_with_me', blank=True, to='app.Player'),
        ),
        migrations.AddField(
            model_name='game',
            name='polymorphic_ctype',
            field=models.ForeignKey(to='contenttypes.ContentType', null=True, related_name='polymorphic_app.game_set+', editable=False),
        ),
        migrations.AddField(
            model_name='drink',
            name='owner',
            field=models.ForeignKey(to='app.Player'),
        ),
    ]
