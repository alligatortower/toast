from django import forms

from .constants import GAME_TYPE_CHOICES
from .models import Drink


class CreateGameForm(forms.Form):
    game_type = forms.ChoiceField(
            choices=GAME_TYPE_CHOICES,
            required=True,
            help_text='Asymmetrical games have not been tested in a while')
    renew_poison = forms.ChoiceField(
            required=False,
            choices=((False, 'Once per game'), (True, 'Once per round')),
    )
    reveal_team = forms.ChoiceField(
            required=False,
            choices=((False, 'Teams stay secret'), (True, "One player's team is revealed at end of round")),
            help_text='Asymmetrical = Random non-host player. Team = Previous host'
    )
    host_force = forms.ChoiceField(
            required=False,
            choices=((False, 'Host cannot force trades'), (True, 'Host can force trades')),
    )
    global_trades = forms.IntegerField(required=False, initial=10, help_text='Number of recent trades this round that everyone can see. Leave blank to disable global trade list')
    minimum_trades = forms.IntegerField(required=False, help_text='Number of trades that must happen before a toast can be proposed. Leave blank to disable minimum required trades per round')
    no_kill_rounds = forms.IntegerField(required=False, initial=2, help_text='number of rounds without a death before the game ends in a draw')

    class Meta:
        fields = ('game_type', 'renew_poison_each_round', 'reveal_teams_each_round', 'list_global_trades', 'minimum_trades', 'host_force', 'no_kill_rounds')


class PlayerNameForm(forms.Form):
    name = forms.CharField()

    class Meta:
        fields = ('name')


class ServeDrinkForm(forms.ModelForm):
    class Meta:
        model = Drink
        fields = ('poisoned', 'icon')


class FindGameForm(forms.Form):
    game_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Game #'}))

    class Meta:
        fields = ('game_number')
