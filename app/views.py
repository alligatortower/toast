from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.http import Http404
from django.utils.translation import ugettext_lazy as _

from .forms import PlayerNameForm, ServeDrinkForm
from .models import Game, Player, Drink
from .constants import TEAM_CHOICES, GAMESTATE_CHOICES


def error(request):
    """for testing purposes"""
    raise Exception


def index(request):
    loyalist_wins = Game.objects.filter(winners=TEAM_CHOICES.LOYALIST).count()
    traitor_wins = Game.objects.filter(winners=TEAM_CHOICES.TRAITOR).count()
    no_wins = Game.objects.filter(winners=None, gamestate=GAMESTATE_CHOICES.ENDED).count()
    total_players = Player.objects.all().count()
    return render(request, 'index.html', {'loyalist_wins': loyalist_wins, 'traitor_wins': traitor_wins, 'no_wins': no_wins, 'total_players': total_players})


def continue_game_view(request):
    session_key = request.session.session_key
    player = Player.objects.filter(session_key=session_key).exclude(game__gamestate=GAMESTATE_CHOICES.ENDED).first()
    if player:
        return redirect('game_detail', pk=player.game.pk)
    messages.error(request, "Sorry, we couldn't find any ongoing games that you're a player in")
    return redirect('index')


def create_game_view(request):
    game = Game.objects.create()
    session_key = request.session.session_key
    Player.objects.create(game=game, session_key=session_key, game_owner=True)
    return redirect('player_name', pk=game.pk)


def start_game_view(request, pk):
    game = get_object_or_404(Game, pk=pk)
    if len(game.player_set.all()) < 2:
        raise Http404(_('You need at least 3 players'))
    session_key = request.session.session_key
    if not session_key:
        raise Http404(_('You need to enable cookies'))
    player = Player.objects.filter(session_key=session_key, game=game).first()
    if not player or not player.game_owner:
        raise Http404(_('Only the person who created the game can start it'))
    game.start_game()
    return redirect('game_detail', pk=game.pk)


def end_game_view(request, pk):
    game = get_object_or_404(Game, pk=pk)
    game.change_gamestate(GAMESTATE_CHOICES.ENDED)
    return redirect('index')


def game_detail_view(request, pk):
    game = get_object_or_404(Game, pk=pk)
    if game.gamestate == GAMESTATE_CHOICES.ENDED:
        return render(request, 'game-over.html', {'you': None, 'game': game})
    session_key = request.session.session_key
    if not session_key:
        raise Http404(_('You need to enable cookies (or refresh, sometimes that works)'))
    player = Player.objects.filter(session_key=session_key, game=game).first()
    if not player:
        if game.gamestate != GAMESTATE_CHOICES.UNSTARTED:
            raise Http404(_('This game has already started, join the next one'))
        player = Player.objects.create(game=game, session_key=session_key)
        return redirect('player_name', game.pk)
    if not player.alive:
        return render(request, 'dead.html', {'you': None, 'game': game})
    successfully_poisoned = request.session.get('successfully_poisoned', False)
    if successfully_poisoned:
        request.session['successfully_poisoned'] = False
    return render(request, 'game-detail.html', {'you': player, 'game': game, 'successfully_poisoned': successfully_poisoned})


def player_name_view(request, pk):
    game = get_object_or_404(Game, pk=pk)
    session_key = request.session.session_key
    player = get_object_or_404(Player, game=game, session_key=session_key)
    if request.method == 'GET':
        form = PlayerNameForm()
        return render(request, 'create_player.html', {'form': form, 'game_pk': pk})
    elif request.method == 'POST':
        form = PlayerNameForm(request.POST)
        if form.is_valid():
            player.name = form.cleaned_data['name']
            player.save()
    return redirect('game_detail', pk=game.pk)


def choose_server_view(request, game_pk, server_pk):
    game = get_object_or_404(Game, pk=game_pk)
    if not game.gamestate == GAMESTATE_CHOICES.CHOOSING:
        raise Http404(_('You cannot choose the server, the game is not in choose state'))
    session_key = request.session.session_key
    player = get_object_or_404(Player, game=game, session_key=session_key)
    if not player.team == TEAM_CHOICES.AMBASSADOR:
        raise Http404(_('Only the ambassador can choose the server'))
    server = get_object_or_404(Player, game=game, pk=server_pk)
    if not server.alive:
        raise Http404(_('Dead people cannot serve drinks'))
    if player == server:
        raise Http404(_('You, the ambassador, cannot serve drinks'))
    server.make_server()
    game.change_gamestate(GAMESTATE_CHOICES.SERVING)
    return redirect('game_detail', pk=game.pk)


def serve_drink_view(request, game_pk, recipient_pk):
    game = get_object_or_404(Game, pk=game_pk)
    if not game.gamestate == GAMESTATE_CHOICES.SERVING:
        raise Http404(_('It is not time to serve the drinks'))
    session_key = request.session.session_key
    player = get_object_or_404(Player, game=game, session_key=session_key)
    if not player.server:
        raise Http404(_('You are not the server'))
    recipient = get_object_or_404(Player, game=game, pk=recipient_pk)
    if not recipient.alive:
        raise Http404(_('You cannot serve a dead person'))
    if recipient.drink_set.all():
        raise Http404(_('This person already has a drink'))
    if request.method == 'GET':
        form = ServeDrinkForm()
        return render(request, 'serve-drink.html', {'form': form, 'recipient': recipient, 'game_pk': game.pk})
    elif request.method == 'POST':
        form = ServeDrinkForm(request.POST)
        if form.is_valid():
            poison = form.cleaned_data['poisoned']
            if poison and (not player.team == TEAM_CHOICES.TRAITOR or not player.has_poison):
                raise Http404(_('You either are not a traitor or do not have poison to use'))
            Drink.objects.create(poisoned=poison, owner=recipient, icon=form.cleaned_data['icon'])
            if poison:
                player.has_poison = False
                player.save()
            still_need_drinks = False
            for player in game.player_set.filter(alive=True):
                if not player.drink_set.all():
                    still_need_drinks = True
            if not still_need_drinks:
                game.change_gamestate(GAMESTATE_CHOICES.TRADING)
                player.no_longer_server()
    return redirect('game_detail', pk=game.pk)


def offer_trade_view(request, game_pk, partner_pk):
    game = get_object_or_404(Game, pk=game_pk)
    if not game.gamestate == GAMESTATE_CHOICES.TRADING:
        raise Http404(_('You cannot offer a trade, the game is not in trade mode'))
    session_key = request.session.session_key
    player = get_object_or_404(Player, game=game, session_key=session_key)
    if not player.alive:
        raise Http404(_('Dead people cannot trade drinks'))
    partner = get_object_or_404(Player, game=game, pk=partner_pk)
    if player.team == TEAM_CHOICES.AMBASSADOR or partner in player.wants_to_trade_with_me.all():
        trade_drinks(player, partner)
    else:
        player.wants_to_trade.add(partner)
        player.save()
    return redirect('game_detail', pk=game.pk)


def trade_drinks(player, partner):
    partner_drink = partner.drink_set.all().first()
    your_drink = player.drink_set.all().first()
    if not partner_drink and your_drink:
        raise Http404(_('One of you does not have a drink'))
    partner_drink.owner = player
    your_drink.owner = partner
    your_drink.save()
    partner_drink.save()
    partner.wants_to_trade.clear()
    player.wants_to_trade.clear()
    partner.wants_to_trade_with_me.clear()
    player.wants_to_trade_with_me.clear()
    player.last_trade = str(partner)
    partner.last_trade = str(player)
    player.save()
    partner.save()


def poison_drink_view(request, pk):
    game = get_object_or_404(Game, pk=pk)
    if not game.gamestate == GAMESTATE_CHOICES.TRADING:
        raise Http404(_('You cannot poison drinks right now'))
    session_key = request.session.session_key
    player = get_object_or_404(Player, game=game, session_key=session_key)
    if not player.alive:
        raise Http404(_('Dead people cannot poison'))
    if not player.has_poison:
        return redirect('game_detail', pk=game.pk)
    player.poison_drink()
    request.session['successfully_poisoned'] = True
    return redirect('game_detail', pk=game.pk)


def propose_toast_view(request, pk):
    game = get_object_or_404(Game, pk=pk)
    if not game.gamestate == GAMESTATE_CHOICES.TRADING:
        raise Http404(_('It is not appropriate to propose a toast right now'))
    session_key = request.session.session_key
    player = get_object_or_404(Player, game=game, session_key=session_key)
    if not player.team == TEAM_CHOICES.AMBASSADOR:
        raise Http404(_('You cannot propose a toast, you are not the ambassador'))
    for player in game.player_set.filter(alive=True):
        player.drink()
        player.wants_to_trade.clear()
        player.wants_to_trade_with_me.clear()
    game.start_next_round()
    return redirect('game_detail', pk=game.pk)
