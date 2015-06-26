from model_utils import Choices
from django.templatetags.static import static
from django.utils.translation import ugettext_lazy as _

TEAMS_THAT_WIN = Choices(
    ('loyalist', 'LOYALIST', _('Loyalist')),
    ('traitor', 'TRAITOR', _('Traitor')),
)
OTHER_TEAMS = Choices(
    ('unassigned', 'UNASSIGNED', _('Unassigned')),
    ('ambassador', 'AMBASSADOR', _('Ambassador')),
    ('dead', 'DEAD', _('Dead')),
)
TEAM_CHOICES = TEAMS_THAT_WIN + OTHER_TEAMS

GAMESTATE_CHOICES = Choices(
    ('unstarted', 'UNSTARTED', _('Unstarted')),
    ('choosing', 'CHOOSING', _('Ambassador is Choosing the server')),
    ('serving', 'SERVING', _('The Server is serving drinks')),
    ('trading', 'TRADING', _('Drinks may be traded until the Toast')),
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
