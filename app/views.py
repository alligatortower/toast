from django.contrib import messages
from django.db.models.loading import get_model
from django.http import Http404
from django.shortcuts import redirect, render, render_to_response, get_object_or_404
from django.utils.translation import ugettext_lazy as _

from app import constants as c
from .forms import CreateGameForm, FindGameForm, PlayerNameForm, ServeDrinkForm
from .models import Game, TeamGame, Player, Drink


def error(request):
    """for testing purposes"""
    raise Exception


def index(request):
    # loyalist_wins = Game.objects.filter(winners=c.TEAM_CHOICES.LOYALIST).count()
    # traitor_wins = Game.objects.filter(winners=C.TEAM_CHOICES.TRAITOR).count()
    # no_wins = Game.objects.filter(winners=None, gamestate=c.GAMESTATE_CHOICES.ENDED).count()
    # total_players = Player.objects.all().count()
    context = {'form': FindGameForm()
        # 'loyalist_wins': loyalist_wins,
        # 'traitor_wins': traitor_wins,
        # 'no_wins': no_wins,
        # 'total_players': total_players,
    }
    return render(request, 'index.html', context)


def create_custom_game_view(request):
    if request.method == 'GET':
        form = CreateGameForm()
    elif request.method == 'POST':
        form = CreateGameForm(request.POST)
        if form.is_valid():
            session_key = request.session.session_key
            game_type = get_model('app', form.cleaned_data['game_type'])
            game = game_type.objects.create(
                    renew_poison_each_round=form.cleaned_data['renew_poison'],
                    reveal_teams_each_round=form.cleaned_data['reveal_team'],
                    list_global_trades=form.cleaned_data['global_trades'],
                    minimum_trades_per_round=form.cleaned_data['minimum_trades'],
                    host_can_force_trades=form.cleaned_data['host_force'],
                    no_kill_rounds_before_draw=form.cleaned_data['no_kill_rounds'],
            )
            game.create_player(session_key=session_key, game_owner=True)
            return redirect('player_name', pk=game.pk)
    return render(request, 'create_game.html', {'form': form})


def create_team_game_view(request):
    session_key = request.session.session_key
    game = TeamGame.objects.create(
            renew_poison_each_round=False,
            reveal_teams_each_round=True,
            list_global_trades=10,
            minimum_trades_per_round=1,
            host_can_force_trades=False,
            no_kill_rounds_before_draw=2,
    )
    game.create_player(session_key=session_key, game_owner=True)
    return redirect('player_name', pk=game.pk)


def find_game_view(request):
    number = request.GET.get('game_number')
    if not number:
        messages.error(request, 'Enter a number')
        return redirect('index')
    if not number.isdigit():
        messages.error(request, 'no letters, only numbers')
        return redirect('index')
    game = Game.objects.filter(pk=number).first()
    if not game:
        messages.error(request, 'A game with that number does not exist')
        return redirect('index')
    return redirect('game_detail', pk=game.pk)


def continue_game_view(request):
    session_key = request.session.session_key
    player = Player.objects.filter(session_key=session_key).exclude(game__gamestate=c.GAMESTATE_CHOICES.ENDED).first()
    if player:
        return redirect('game_detail', pk=player.game.pk)
    messages.error(request, "Sorry, we couldn't find any ongoing games that you're a player in")
    return redirect('index')


def start_game_view(request, pk):
    game = get_object_or_404(Game, pk=pk)
    if len(game.player_set.all()) < 2:
        messages.error(request, "You can't start a game with only one player")
        return redirect('game_detail', pk=game.pk)
    session_key = request.session.session_key
    if not session_key:
        raise Http404("You need to set cookies, try refreshing the page")
    player = Player.objects.filter(session_key=session_key, game=game).first()
    if not player or not player.game_owner:
        messages.error(request, 'Only the person who created the game can start it')
        return redirect('game_detail', pk=game.pk)
    game.start_game()
    return redirect('game_detail', pk=game.pk)


def end_game_view(request, pk):
    game = get_object_or_404(Game, pk=pk)
    game.change_gamestate(c.GAMESTATE_CHOICES.ENDED)
    return redirect('index')


def game_detail_view(request, pk):
    game = get_object_or_404(Game, pk=pk)
    if game.gamestate == c.GAMESTATE_CHOICES.ENDED:
        context = {'you': None, 'game': game}
        if request.is_ajax():
            return render_to_response('snippets/game-over-body.html', context)
        return render(request, 'game-over.html', context)
    session_key = request.session.session_key
    if not session_key:
        raise Http404(_('You need to enable cookies (or refresh, sometimes that works)'))
    player = Player.objects.filter(session_key=session_key, game=game).first()
    if not player:
        if not game.gamestate == c.GAMESTATE_CHOICES.UNSTARTED:
            raise Http404(_('This game has already started, join the next one'))
        player = game.create_player(session_key)
        return redirect('player_name', game.pk)
    if not player.alive:
        context = {'you': None, 'game': game}
        if request.is_ajax():
            return render_to_response('snippets/dead-body.html', context)
        return render(request, 'dead.html', context)
    successfully_poisoned = request.session.get('successfully_poisoned', False)
    if successfully_poisoned:
        request.session['successfully_poisoned'] = False
    context = {'you': player, 'game': game, 'successfully_poisoned': successfully_poisoned}
    if request.is_ajax():
        return render_to_response('snippets/game-meat.html', context)
    return render(request, 'game-detail.html', context)


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
    if not game.gamestate == c.GAMESTATE_CHOICES.CHOOSING:
        messages.error(request, 'You cannot choose the server, the game is not in choose state')
        return redirect('game_detail', pk=game.pk)
    session_key = request.session.session_key
    player = get_object_or_404(Player, alive=True, game=game, session_key=session_key)
    if not player.host:
        messages.error(request, 'Only the host can choose the server')
        return redirect('game_detail', pk=game.pk)
    server = get_object_or_404(Player, alive=True, game=game, pk=server_pk)
    if player == server:
        messages.error(request, 'You, the host, cannot serve drinks')
        return redirect('game_detail', pk=game.pk)
    server.make_server()
    game.change_gamestate(c.GAMESTATE_CHOICES.SERVING)
    return redirect('game_detail', pk=game.pk)


def serve_drink_view(request, game_pk, recipient_pk):
    game = get_object_or_404(Game, pk=game_pk)
    if not game.gamestate == c.GAMESTATE_CHOICES.SERVING:
        messages.error(request, 'It is not time to serve the drinks')
        return redirect('game_detail', pk=game.pk)
    session_key = request.session.session_key
    player = get_object_or_404(Player, game=game, session_key=session_key)
    if not player.server:
        messages.error(request, 'You are not the server')
        return redirect('game_detail', pk=game.pk)
    recipient = get_object_or_404(Player, alive=True, game=game, pk=recipient_pk)
    if recipient.drink_set.all():
        messages.error(request, 'This person already has a drink')
        return redirect('game_detail', pk=game.pk)
    if request.method == 'GET':
        form = ServeDrinkForm()
        return render(request, 'serve-drink.html', {'form': form, 'recipient': recipient, 'game_pk': game.pk})
    elif request.method == 'POST':
        form = ServeDrinkForm(request.POST)
        if form.is_valid():
            poison = form.cleaned_data['poisoned']
            if poison and not player.has_poison:
                messages.error(request, 'You do not have any poison to use so you cannot poison a drink')
                return render(request, 'serve-drink.html', {'form': form, 'recipient': recipient, 'game_pk': game.pk})
            Drink.objects.create(poisoned=poison, owner=recipient, icon=form.cleaned_data['icon'])
            if poison:
                player.has_poison = False
                player.save()
            still_need_drinks = False
            for player in game.player_set.filter(alive=True):
                if not player.drink_set.all():
                    still_need_drinks = True
            if not still_need_drinks:
                game.change_gamestate(c.GAMESTATE_CHOICES.TRADING)
                for player in game.player_set.filter(server=True):
                    player.server = False
                    player.save()
    return redirect('game_detail', pk=game.pk)


def offer_trade_view(request, game_pk, partner_pk):
    game = get_object_or_404(Game, pk=game_pk)
    if game.gamestate not in [c.GAMESTATE_CHOICES.TRADING, c.GAMESTATE_CHOICES.PROPOSED]:
        messages.error(request, 'You cannot offer a trade, the game is not in trade mode')
        return redirect('game_detail', pk=game.pk)
    session_key = request.session.session_key
    offerer = get_object_or_404(Player, alive=True, game=game, session_key=session_key)
    receiver = get_object_or_404(Player, alive=True, game=game, pk=partner_pk)
    message = game.facilitate_trade(offerer, receiver)
    if message:
        messages.error(request, message)
    return redirect('game_detail', pk=game.pk)


def poison_drink_view(request, pk):
    game = get_object_or_404(Game, pk=pk)
    if not game.gamestate == c.GAMESTATE_CHOICES.TRADING:
        messages.error(request, 'You can only poison drinks after everyone has been served, while waiting for the toast')
        return redirect('game_detail', pk=game.pk)
    session_key = request.session.session_key
    player = get_object_or_404(Player, alive=True, game=game, session_key=session_key)
    if not player.has_poison:
        return redirect('game_detail', pk=game.pk)
    player.poison_drink()
    request.session['successfully_poisoned'] = True
    return redirect('game_detail', pk=game.pk)


def propose_toast_view(request, pk):
    game = get_object_or_404(Game, pk=pk)
    session_key = request.session.session_key
    player = get_object_or_404(Player, game=game, session_key=session_key)
    if not player.host:
        messages.error(request, 'You cannot propose a toast, you are not the host')
        return redirect('game_detail', pk=game.pk)
    if not game.gamestate == c.GAMESTATE_CHOICES.TRADING:
        messages.error(request, 'It is not appropriate to propose a toast right now')
        return redirect('game_detail', pk=game.pk)
    message = game.toast_proposed(player)
    if message:
        messages.error(request, message)
    return redirect('game_detail', pk=game.pk)


def raise_drink_view(request, pk):
    game = get_object_or_404(Game, pk=pk)
    session_key = request.session.session_key
    player = get_object_or_404(Player, game=game, session_key=session_key)
    if not game.gamestate == c.GAMESTATE_CHOICES.PROPOSED:
        messages.error(request, 'Why are you raising your drink?')
        return redirect('game_detail', pk=game.pk)
    if player.host:
        messages.error(request, 'You are the host')
        return redirect('game_detail', pk=game.pk)
    if player.drink_raised:
        messages.error(request, 'Your drink is already raised')
        return redirect('game_detail', pk=game.pk)
    player.raise_drink()
    all_drinks_raised = True
    for player in game.player_set.filter(alive=True):
        if not player.drink_raised:
            all_drinks_raised = False
    if all_drinks_raised:
        game.change_gamestate(c.GAMESTATE_CHOICES.TOAST)
    return redirect('game_detail', pk=game.pk)


def toast_view(request, pk):
    game = get_object_or_404(Game, pk=pk)
    session_key = request.session.session_key
    player = get_object_or_404(Player, game=game, session_key=session_key)
    if not game.gamestate == c.GAMESTATE_CHOICES.TOAST:
        messages.error(request, 'Now is not the time to toast')
        return redirect('game_detail', pk=game.pk)
    if not player.host:
        messages.error(request, 'Only the host can toast')
        return redirect('game_detail', pk=game.pk)
    game.start_next_round()
    return redirect('game_detail', pk=game.pk)
