from model_utils import Choices
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
    ('choosing', 'CHOOSING', _('Waiting for Ambassador to choose server')),
    ('serving', 'SERVING', _('Waiting for server to serve drinks')),
    ('trading', 'TRADING', _('Waiting for Ambassador to propose toast')),
    ('ended', 'ENDED', _('Ended')),
)
