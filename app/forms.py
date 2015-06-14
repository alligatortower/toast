from django import forms


class PlayerNameForm(forms.Form):
    name = forms.CharField()

    class Meta:
        fields = ('name')
