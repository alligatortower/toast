import random
from django.db import models
from polymorphic import PolymorphicModel

from model_utils.models import TimeStampedModel
# from django_extensions.db.models import AutoSlugField

from app import constants


class Game(PolymorphicModel, TimeStampedModel):
    gamestate = models.CharField(max_length=200, choices=constants.GAMESTATE_CHOICES, default=constants.GAMESTATE_CHOICES.UNSTARTED)
    host = models.BooleanField(default=False)

    def start_game(self):
        raise NotImplementedError

    def start_next_round(self):
        raise NotImplementedError

    def create_player(self):
        raise NotImplementedError

    def change_gamestate(self, state):
        if state == 'trading':
            for player in self.player_set.all():
                player.server = False
                player.save()
        self.gamestate = state
        self.save()

    @property
    def gamestate_display(self):
        return str(constants.GAMESTATE_CHOICES[self.gamestate])


class Player(PolymorphicModel, TimeStampedModel):
    game = models.ForeignKey('Game')
    wants_to_trade = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='wants_to_trade_with_me')
    name = models.CharField(max_length=200, blank=True, null=True)
    session_key = models.CharField(max_length=200)
    alive = models.BooleanField(default=True)
    has_poison = models.BooleanField(default=False)
    server = models.BooleanField(default=False)
    game_owner = models.BooleanField(default=False)
    last_trade = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        ordering = ('created',)

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

    def renew_poison(self):
        self.has_poison = True
        self.save()

    def kill(self):
        self.alive = False
        self.has_poison = False
        self.team = constants.BASE_TEAMS.DEAD
        self.save()

    def poison_drink(self):
        drink = self.drink_set.all()[0]
        drink.poisoned = True
        drink.save()
        self.has_poison = False
        self.save()

    def drink(self):
        drink = self.drink_set.all()[0]
        if drink.poisoned:
            self.kill()
        drink.delete()

    @property
    def team_display(self):
        return str(constants.TEAM_CHOICES[self.team])


class AsymmetricalGame(Game):
    winners = models.CharField(max_length=200, choices=constants.ASYMMETRICAL_TEAMS, blank=True, null=True)

    def start_game(self):
        players = list(self.player_set.all())
        host_index = random.randrange(1, len(players))
        host = players.pop(host_index)
        host.make_host()
        host.set_team(constants.ASYMMETRICAL_TEAMS.LOYALIST)
        # for two player games:
        if len(players) == 1:
            player = players[0]
            player.set_team(constants.ASYMMETRICAL_TEAMS.TRAITOR)
            player.renew_poison()
        else:
            loyalist = True
            while len(players) > 0:
                player_count = len(players)
                random_player_index = random.randrange(0, player_count)
                player = players.pop(random_player_index)
                player.set_team(constants.ASYMMETRICAL_TEAMS.LOYALIST) if loyalist else player.set_team(constants.ASYMMETRICAL_TEAMS.TRAITOR)
                if player.team == constants.ASYMMETRICAL_TEAMS.TRAITOR:
                    player.renew_poison()
                loyalist = not loyalist

        self.change_gamestate(constants.GAMESTATE_CHOICES.CHOOSING)
        self.save()

    def start_next_round(self):
        if not self.player_set.filter(team=constants.ASTYMMETRICAL_TEAMS.TRAITOR, alive=True):
            self.change_gamestate(constants.GAMESTATE_CHOICES.ENDED)
            self.winners = constants.TEAMS_THAT_WIN.LOYALIST
            self.save()
        elif not self.player_set.filter(host=True, alive=True):
            self.change_gamestate(constants.GAMESTATE_CHOICES.ENDED)
            self.winners = constants.ASYMMETRICAL_TEAMS.TRAITOR
            self.save()
        else:
            for player in self.player_set.all():
                if player.team == constants.ASYMMETRICAL_TEAMS.TRAITOR and player.alive:
                    player.renew_poison()
                player.last_trade = None
                player.save()
            self.change_gamestate(constants.GAMESTATE_CHOICES.CHOOSING)

    def create_player(self, session_key, game_owner=False):
        return AsymmetricalPlayer.objects.create(game=self, game_owner=game_owner, session_key=session_key)


class TeamGame(Game):
    winners = models.CharField(max_length=200, choices=constants.EQUAL_TEAMS, blank=True, null=True)


class AsymmetricalPlayer(Player):
    team = models.CharField(max_length=20, choices=constants.ASYMMETRICAL_TEAMS, blank=True, null=True)


class TeamPlayer(Player):
    team = models.CharField(max_length=20, choices=constants.EQUAL_TEAMS, blank=True, null=True)


class Drink(models.Model):
    owner = models.ForeignKey('Player')
    poisoned = models.BooleanField(default=False)
    icon = models.CharField(max_length=200, choices=constants.DRINK_ICON_CHOICES, default=constants.DRINK_ICON_CHOICES.DEFAULT)
