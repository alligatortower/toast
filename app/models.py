import random
from django.db import models
# from django_extensions.db.models import AutoSlugField

from model_utils.models import TimeStampedModel

from .constants import TEAMS_THAT_WIN, TEAM_CHOICES, GAMESTATE_CHOICES, DRINK_ICON_CHOICES


class Game(TimeStampedModel):
    gamestate = models.CharField(max_length=200, choices=GAMESTATE_CHOICES, default=GAMESTATE_CHOICES.UNSTARTED)
    winners = models.CharField(max_length=200, choices=TEAMS_THAT_WIN, blank=True, null=True)

    def start_game(self):
        players = list(self.player_set.all())
        ambassador_index = random.randrange(1, len(players))
        ambassador = players.pop(ambassador_index)
        ambassador.set_team(TEAM_CHOICES.AMBASSADOR)
        loyalist = True
        while len(players) > 0:
            player_count = len(players)
            random_player_index = random.randrange(0, player_count)
            player = players.pop(random_player_index)
            player.set_team(TEAM_CHOICES.LOYALIST) if loyalist else player.set_team(TEAM_CHOICES.TRAITOR)
            if player.team == TEAM_CHOICES.TRAITOR:
                player.renew_poison()
            loyalist = not loyalist

        self.change_gamestate(GAMESTATE_CHOICES.CHOOSING)
        self.save()

    def start_next_round(self):
        if not self.player_set.filter(team=TEAM_CHOICES.TRAITOR, alive=True):
            self.change_gamestate(GAMESTATE_CHOICES.ENDED)
            self.winners = TEAMS_THAT_WIN.LOYALIST
            self.save()
        elif not self.player_set.filter(team=TEAM_CHOICES.AMBASSADOR, alive=True):
            self.change_gamestate(GAMESTATE_CHOICES.ENDED)
            self.winners = TEAMS_THAT_WIN.TRAITOR
            self.save()
        else:
            for player in self.player_set.all():
                if player.team == TEAM_CHOICES.TRAITOR and player.alive:
                    player.renew_poison()
                player.last_trade = None
                player.save()
            self.change_gamestate(GAMESTATE_CHOICES.CHOOSING)

    def change_gamestate(self, state):
        self.gamestate = state
        self.save()


class Player(TimeStampedModel):
    game = models.ForeignKey('Game')
    team = models.CharField(max_length=20, choices=TEAM_CHOICES, default=TEAM_CHOICES.UNASSIGNED)
    wants_to_trade = models.ManyToManyField('self', symmetrical=False, blank=True, null=True, related_name='wants_to_trade_with_me')
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

    def no_longer_server(self):
        self.server = False
        self.save()

    def renew_poison(self):
        self.has_poison = True
        self.save()

    def kill(self):
        self.alive = False
        self.has_poison = False
        self.team = TEAM_CHOICES.DEAD
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


class Drink(models.Model):
    owner = models.ForeignKey('Player')
    poisoned = models.BooleanField(default=False)
    icon = models.CharField(max_length=200, choices=DRINK_ICON_CHOICES, default=DRINK_ICON_CHOICES.DEFAULT)
