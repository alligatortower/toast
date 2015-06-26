from django.conf.urls import url
from django.views.generic import TemplateView

from app import views

urlpatterns = [
    url(r'^error/', views.error, name='error'),
    url(r'^$', views.index, name='index'),
    url(r'^rules/$', TemplateView.as_view(template_name='rules.html'), name='rules'),
    url(r'^continue/$', views.continue_game_view, name='continue'),
    url(r'^creategame/$', views.create_game_view, name='create_game'),
    url(r'^findgame/$', views.find_game_view, name='find_game'),
    url(r'^game/(?P<pk>[-_\w]+)/start/$', views.start_game_view, name='start_game'),
    url(r'^game/(?P<pk>[-_\w]+)/player_name/$', views.player_name_view, name='player_name'),
    url(r'^game/(?P<pk>[-_\w]+)/end/$', views.end_game_view, name='end_game'),
    url(r'^game/(?P<pk>[-_\w]+)/$', views.game_detail_view, name='game_detail'),
    url(r'^game/(?P<game_pk>[-_\w]+)/choose/(?P<server_pk>[-_\w]+)/$', views.choose_server_view, name='choose_server'),
    url(r'^game/(?P<game_pk>[-_\w]+)/serve/(?P<recipient_pk>[-_\w]+)/$', views.serve_drink_view, name='serve_drink'),
    url(r'^game/(?P<game_pk>[-_\w]+)/trade/(?P<partner_pk>[-_\w]+)/$', views.offer_trade_view, name='offer_trade'),
    url(r'^game/(?P<pk>[-_\w]+)/poison$', views.poison_drink_view, name='poison_drink'),
    url(r'^game/(?P<pk>[-_\w]+)/toast$', views.propose_toast_view, name='propose_toast'),


]

from .signals import *  # NOQA ensure that the signals are attatched via import
