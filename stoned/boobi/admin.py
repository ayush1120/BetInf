from django.contrib import admin
from boobi.models import *
# Register your models here.

class SportAdmin(admin.ModelAdmin):
    pass

class TeamAdmin(admin.ModelAdmin):
    pass

class MatchAdmin(admin.ModelAdmin):
    pass

class BetAdmin(admin.ModelAdmin):
    pass

class SetAdmin(admin.ModelAdmin):
    pass

admin.site.register(Sport, SportAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(Bet, BetAdmin)
admin.site.register(Set, SetAdmin)