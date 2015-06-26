from django import forms

from .models import Drink


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
