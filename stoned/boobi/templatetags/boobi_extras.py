from django import template
from boobi.models import Match, Game
register = template.Library()

@register.filter
def matchgames(games, match_pk):
    out_games = Game.objects.all().filter(match=Match.objects.get(match_pk=match_pk)) 
    return out_games

@register.filter
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)