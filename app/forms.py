from django import forms

from .constants import GAME_TYPE_CHOICES
from .models import Drink


class CreateGameForm(forms.Form):
    game_type = forms.ChoiceField(choices=GAME_TYPE_CHOICES, required=True)

    class Meta:
        fields = ('game_type',)


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
