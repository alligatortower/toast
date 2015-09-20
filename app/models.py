import random
from django.db import models
from django.db.models.loading import get_model
from polymorphic import PolymorphicModel

from model_utils.models import TimeStampedModel
# from django_extensions.db.models import AutoSlugField

from app import constants as c


class Game(PolymorphicModel, TimeStampedModel):
    gamestate = models.CharField(max_length=200, choices=c.GAMESTATE_CHOICES, default=c.GAMESTATE_CHOICES.UNSTARTED)
    winners = models.CharField(max_length=200, blank=True, null=True)
    renew_poison_each_round = models.BooleanField(default=False)
    reveal_teams_each_round = models.BooleanField(default=False)
    list_global_trades = models.PositiveSmallIntegerField(help_text='leave blank to disable', blank=True, null=True)
    minimum_trades_per_round = models.PositiveSmallIntegerField(blank=True, null=True)
    host_can_force_trades = models.BooleanField(default=True)
    no_kill_rounds_before_draw = models.PositiveSmallIntegerField(blank=True, null=True)
    rounds_without_kill = models.PositiveSmallIntegerField(default=0)

    def start_game(self):
        raise NotImplementedError

    def start_next_round(self):
        raise NotImplementedError

    def facilitate_trade(self, offerer, receiver):
        if (offerer.host and self.host_can_force_trades and not self.gamestate == 'toast_proposed') or receiver in offerer.wants_to_trade_with_me.all():
            trade_complete = self.trade_drinks(offerer, receiver)
            if not trade_complete:
                return 'The trade was not compeleted'
        elif self.gamestate == c.GAMESTATE_CHOICES.PROPOSED:
            return 'You cannot offer any new trades now that the toast has been proposed'
        else:
            offerer.wants_to_trade.add(receiver)
            offerer.save()
        return False

    def trade_drinks(self, offerer, receiver):
        receiver_drink = receiver.drink_set.all().first()
        offerer_drink = offerer.drink_set.all().first()
        if not receiver_drink and offerer_drink:
            return False
        receiver_drink.owner = offerer
        offerer_drink.owner = receiver
        offerer_drink.save()
        receiver_drink.save()
        receiver.wants_to_trade.clear()
        offerer.wants_to_trade.clear()
        receiver.wants_to_trade_with_me.clear()
        offerer.wants_to_trade_with_me.clear()
        offerer.last_trade = str(receiver)
        receiver.last_trade = str(offerer)
        offerer.save()
        receiver.save()
        #offerer/receiver reversed because confusion is fun and also because the original offerer is now the receiver etc.
        TradeRecord.objects.create(game=self, offerer=receiver, receiver=offerer)
        return True

    def toast_proposed(self, host):
        trades = self.traderecord_set.count()
        if self.minimum_trades_per_round and not trades >= self.minimum_trades_per_round:
            return "Only {0} trades have happened this round, You cannot propose a toast until {1} trades have happened".format(trades, self.minimum_trades_per_round)
        host.raise_drink()
        self.change_gamestate(c.GAMESTATE_CHOICES.PROPOSED)
        return False

    def remove_traderecords(self):
        for record in self.traderecord_set.all():
            record.delete()

    @property
    def gamestate_display(self):
        return str(c.GAMESTATE_CHOICES[self.gamestate])

    @property
    def trade_record(self):
        if self.list_global_trades:
            trades = self.traderecord_set.all()[:self.list_global_trades]
            return ["{0} traded with {1}".format(trade.offerer, trade.receiver) for trade in trades]
        return []

    def change_gamestate(self, state):
        self.gamestate = state
        self.save()

    def set_winners(self, winner):
        self.winners = winner
        self.save()

    def create_player(self, session_key, game_owner=False):
        if not self.player_model:
            raise AttributeError('class "{0}" has no player_model attribute'.format(self.__class__.__name__))
        player_model = get_model('app', self.player_model)
        return player_model.objects.create(game=self, game_owner=game_owner, session_key=session_key)

    def alive_on_team(self, team):
        player_model = get_model('app', self.player_model)
        return bool(player_model.objects.filter(team=team, alive=True))

    def update_rounds_without_kill(self, pre_players, post_players):
        if pre_players == post_players:
            self.rounds_without_kill += 1
        else:
            self.rounds_without_kill = 0
        self.save()


class Player(PolymorphicModel, TimeStampedModel):
    game = models.ForeignKey('Game')
    host = models.BooleanField(default=False)
    wants_to_trade = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='wants_to_trade_with_me')
    name = models.CharField(max_length=200, blank=True, null=True)
    session_key = models.CharField(max_length=200)
    alive = models.BooleanField(default=True)
    has_poison = models.BooleanField(default=False)
    server = models.BooleanField(default=False)
    drink_raised = models.BooleanField(default=False)
    game_owner = models.BooleanField(default=False)
    last_trade = models.CharField(max_length=200, blank=True, null=True)
    team_revealed = models.BooleanField(default=False)

    class Meta:
        ordering = ('created',)
        get_latest_by = 'created'

    def __str__(self):
        return self.name if self.name else str(self.pk)

    def set_team(self, team):
        self.team = team
        self.save()

    def make_server(self):
        self.server = True
        self.save()

    def make_host(self):
        self.host = True
        self.save()

    def remove_host(self, reveal_team=False):
        if reveal_team:
            self.reveal_team()
        self.host = False
        self.save()

    def reveal_team(self):
        self.team_revealed = True
        self.save()

    def renew_poison(self):
        self.has_poison = True
        self.save()

    def raise_drink(self):
        self.drink_raised = True
        self.save()

    def kill(self):
        self.alive = False
        self.save()

    def poison_drink(self):
        drink = self.drink_set.all()[0]
        drink.poisoned = True
        drink.save()
        self.has_poison = False
        self.save()

    def drink(self, renew_poison=False):
        if renew_poison:
            self.renew_poison()
        self.wants_to_trade.clear()
        self.wants_to_trade_with_me.clear()
        self.last_trade = None
        self.drink_raised = False
        self.save()

        drink = self.drink_set.first()
        if drink.poisoned:
            self.kill()
        drink.delete()

    @property
    def team_display(self):
        return str(c.TEAM_CHOICES[self.team])

    @property
    def team_short_display(self):
        return self.team_display.upper()[:1]


class AsymmetricalGame(Game):
    player_model = 'AsymmetricalPlayer'

    def start_game(self):
        players = list(self.player_set.all())
        host_index = random.randrange(1, len(players))
        host = players.pop(host_index)
        host.make_host()
        host.set_team(c.ASYMMETRICAL_TEAMS.LOYALIST)
        # for two player games:
        if len(players) == 1:
            player = players[0]
            player.set_team(c.ASYMMETRICAL_TEAMS.TRAITOR)
            player.renew_poison()
        else:
            loyalist = True
            while len(players) > 0:
                player_count = len(players)
                random_player_index = random.randrange(0, player_count)
                player = players.pop(random_player_index)
                player.set_team(c.ASYMMETRICAL_TEAMS.LOYALIST) if loyalist else player.set_team(c.ASYMMETRICAL_TEAMS.TRAITOR)
                if player.team == c.ASYMMETRICAL_TEAMS.TRAITOR:
                    player.renew_poison()
                loyalist = not loyalist

        self.change_gamestate(c.GAMESTATE_CHOICES.CHOOSING)
        self.save()

    def start_next_round(self):
        live_players = self.player_set.filter(alive=True)
        for player in live_players:
            renew_poison = bool(player.team == c.ASYMMETRICAL_TEAMS.TRAITOR and self.renew_poison_each_round)
            player.drink(renew_poison=renew_poison)
        live_players_after_drinking = self.player_set.filter(alive=True).count()
        self.update_rounds_without_kill(live_players.count(), live_players_after_drinking)
        if not self.alive_on_team(c.ASTYMMETRICAL_TEAMS.TRAITOR):
            self.change_gamestate(c.GAMESTATE_CHOICES.ENDED)
            self.winners = c.TEAM_CHOICES.LOYALIST
            self.save()
        elif not self.player_set.filter(host=True, alive=True):
            self.change_gamestate(c.GAMESTATE_CHOICES.ENDED)
            self.winners = c.ASYMMETRICAL_TEAMS.TRAITOR
            self.save()
        elif not self.renew_poison_each_round and not self.player_set.filter(alive=True, has_poison=True):
            self.change_gamestate(c.GAMESTATE_CHOICES.ENDED)
            self.set_winners('Draw, no poison left')
            self.save()
        elif self.rounds_without_kill >= self.no_kill_rounds_before_draw:
            self.change_gamestate(c.GAMESTATE_CHOICES.ENDED)
            self.set_winners('Draw, {0} rounds without anyone dying'.format(self.rounds_without_kill))
            self.save()
        else:
            if self.reveal_teams_each_round:
                players = self.player_set.filter(alive=True, host=False, team_revealed=False)
                players[random.randrange(0, len(players))].reveal_team()
            self.remove_traderecords()
            self.change_gamestate(c.GAMESTATE_CHOICES.CHOOSING)


class TeamGame(Game):
    player_model = 'TeamPlayer'

    def start_game(self):
        players = list(self.player_set.all())
        empire = random.randrange(0, 1)
        while len(players) > 0:
            player_count = len(players)
            random_player_index = random.randrange(0, player_count)
            player = players.pop(random_player_index)
            player.set_team(c.EQUAL_TEAMS.EMPIRE) if empire else player.set_team(c.EQUAL_TEAMS.REPUBLIC)
            player.renew_poison()
            empire = not empire

        players = list(self.player_set.all())
        random_player_index = random.randrange(0, len(players))
        players.pop(random_player_index).make_host()
        self.change_gamestate(c.GAMESTATE_CHOICES.CHOOSING)
        self.save()

    def start_next_round(self):
        live_players = self.player_set.filter(alive=True)
        for player in live_players:
            player.drink(renew_poison=self.renew_poison_each_round)
        live_players_after_drinking = self.player_set.filter(alive=True).count()
        self.update_rounds_without_kill(live_players.count(), live_players_after_drinking)
        empire_alive = self.alive_on_team(c.EQUAL_TEAMS.EMPIRE)
        republic_alive = self.alive_on_team(c.EQUAL_TEAMS.REPUBLIC)
        if not empire_alive or not republic_alive:
            self.change_gamestate(c.GAMESTATE_CHOICES.ENDED)
            self.set_winners(c.TEAM_CHOICES.REPUBLIC if republic_alive else c.TEAM_CHOICES.EMPIRE)
        elif not self.renew_poison_each_round and not self.player_set.filter(alive=True, has_poison=True):
            self.change_gamestate(c.GAMESTATE_CHOICES.ENDED)
            self.set_winners('Draw, no poison left')
        elif self.rounds_without_kill >= self.no_kill_rounds_before_draw:
            self.change_gamestate(c.GAMESTATE_CHOICES.ENDED)
            self.set_winners('Draw, {0} rounds without anyone dying'.format(self.rounds_without_kill))
            self.save()
        else:
            host = self.player_set.filter(host=True).first()
            host.remove_host(reveal_team=self.reveal_teams_each_round)
            # this is bad but ehhhh
            try:
                new_host = host.get_next_by_created(alive=True)
            except:
                new_host = self.player_set.filter(alive=True).earliest()
            new_host.make_host()
            self.remove_traderecords()
            self.change_gamestate(c.GAMESTATE_CHOICES.CHOOSING)


class AsymmetricalPlayer(Player):
    team = models.CharField(max_length=20, choices=c.ASYMMETRICAL_TEAMS, blank=True, null=True)


class TeamPlayer(Player):
    team = models.CharField(max_length=20, choices=c.EQUAL_TEAMS, blank=True, null=True)


class Drink(models.Model):
    owner = models.ForeignKey('Player')
    poisoned = models.BooleanField(default=False)
    icon = models.CharField(max_length=200, choices=c.DRINK_ICON_CHOICES, default=c.DRINK_ICON_CHOICES.DEFAULT)


class TradeRecord(TimeStampedModel):
    game = models.ForeignKey(Game)
    offerer = models.ForeignKey(Player, related_name='offerer')
    receiver = models.ForeignKey(Player, related_name='receiver')

    class Meta:
        ordering = ('-created',)
