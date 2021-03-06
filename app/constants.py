from model_utils import Choices
from django.templatetags.static import static
from django.utils.translation import ugettext_lazy as _

ASYMMETRICAL_TEAMS = Choices(
    ('loyalist', 'LOYALIST', _('Loyalist')),
    ('traitor', 'TRAITOR', _('Traitor')),
)

EQUAL_TEAMS = Choices(
    ('empire', 'EMPIRE', _('Empire')),
    ('republic', 'REPUBLIC', _('Republic')),
)

TEAM_CHOICES = ASYMMETRICAL_TEAMS + EQUAL_TEAMS

#make DB value equal class name
GAME_TYPE_CHOICES = Choices(
    ('AsymmetricalGame', 'ASYMMETRICAL', _('Asymmetrical')),
    ('TeamGame', 'TEAM', _('Team')),
)

GAMESTATE_CHOICES = Choices(
    ('unstarted', 'UNSTARTED', _('Unstarted')),
    ('choosing', 'CHOOSING', _('The Host is Choosing the Server')),
    ('serving', 'SERVING', _('The Server is serving drinks')),
    ('trading', 'TRADING', _('Drinks may be traded until the Toast')),
    ('toast_proposed', 'PROPOSED', _('All drinks must be raised to toast')),
    ('toast', 'TOAST', _('All drinks must be raised to toast')),
    ('ended', 'ENDED', _('Ended')),
)
DRINK_ICON_CHOICES = Choices(
    (static('img/drink-icons/beer-bottle.png'), 'DEFAULT', _('Beer Bottle')),
    (static('img/drink-icons/can.png'), _('Beer Can')),
    (static('img/drink-icons/champagne.png'), _('Champagne')),
    (static('img/drink-icons/cocktail.png'), _('Cocktail')),
    (static('img/drink-icons/coffee.png'), _('Coffee')),
    (static('img/drink-icons/milk.png'), _('Milk')),
    (static('img/drink-icons/on-rocks.png'), _('On the Rocks')),
    (static('img/drink-icons/orange-slice.png'), _('Old Fashioned')),
    (static('img/drink-icons/pint.png'), _('Pint')),
    (static('img/drink-icons/tropical.png'), _('Tropical')),
    (static('img/drink-icons/wedge-on-rim.png'), _('With a wedge')),
    (static('img/drink-icons/wine.png'), _('Wine')),
)
GAMESTATES_THAT_ALLOW_TRADING = ['trading', 'toast_proposed']
