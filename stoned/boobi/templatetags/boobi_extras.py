from django import template
from boobi.models import Match, Set
register = template.Library()

@register.filter
def matchsets(sets, match_pk):
    out_sets = Set.objects.all().filter(match=Match.objects.get(match_pk=match_pk)) 
    return out_sets

@register.filter
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)