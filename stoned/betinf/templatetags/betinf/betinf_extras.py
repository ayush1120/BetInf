from django import template
from betinf.models import Match, Game
register = template.Library()

@register.filter
def matchgames(games, match_pk):
    out_games = Game.objects.all().filter(match=Match.objects.get(match_pk=match_pk)) 
    return out_games

@register.filter
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)

@register.filter
def set_team1_score(sets, game):
    game = Game.objects.get(game_pk=game.game_pk)
    a = sets.filter(game=game, set_num=game.num_sets)
    if len(list(a))>0:
        return a[0].team1_score
    return -1




@register.filter
def set_team2_score(sets, game):
    game = Game.objects.get(game_pk=game.game_pk)
    a = sets.filter(game=game, set_num=game.num_sets)
    if len(list(a))>0:
        return a[0].team2_score
    return -1