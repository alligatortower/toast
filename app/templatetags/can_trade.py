from django.template import Library

from app import constants as c

register = Library()


@register.assignment_tag
def can_trade(you, gamestate='trading', player=None):
    if gamestate not in c.GAMESTATES_THAT_ALLOW_TRADING:
        return False
    if not you.alive or you.drink_raised or player == you:
        return False
    elif player in you.wants_to_trade_with_me.all():
        return 'Wants Trade'
    else:
        return 'Trade'
