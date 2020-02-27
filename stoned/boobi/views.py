from django.shortcuts import render, redirect
# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from .models import *
import os
import shutil
import json
import datetime

import signal
import random
import uuid
from stoned.settings import BASE_DIR, STATICFILES_DIRS, MEDIA_URL
from boobi.models import Match

def show_home(request):
    matches = Match.objects.all()
    # for match in matches:
    #     if match.team1.logo != None:
    #         print(str(match.team1.logo.url))
    #         print(str(match.team1.logo.url))
    return render(request, 'index.html', {
        'matches' : matches,
        "MEDIA_URL" : MEDIA_URL
    })


def show_bet_form(request):
    match_pk = request.POST.get("match_pk")
    match = Match.objects.get(match_pk=match_pk)
    if not request.user.is_authenticated:
        return redirect('home')
    
    return render(request, 'bet.html',{
        'match' : match
    })


def signIn(request):
    if request.method=='POST':
        pass
    return render(request, 'signin.html')


@csrf_exempt
def updateMatch(request):
    matches = Match.objects.all()
    match_pk = int(request.POST.get("match_pk"))
    team_num = int(request.POST.get("team_num"))
    inc = int(request.POST.get("inc"))
    print("match_pk : ", match_pk)
    print("team_num : ", team_num)
    print("inc : ", inc)
    match = Match.objects.get(match_pk=match_pk)
    if team_num==1:
        if inc==1:
            match.team1_score += 1
            match.save()
        else:
            match.team1_score -= 1
            match.save()
    else:
        if inc==1:
            match.team2_score += 1
            match.save()
        else:
            match.team2_score -= 1
            match.save()

    print("match : ")
    print("team1 : ", match.team1_score)
    print("team2 : ", match.team2_score)
    
    return render(request, 'index.html', {
        'matches' : matches,
        "MEDIA_URL" : MEDIA_URL
    })


def show_confirm_form(request):
    if not request.user.is_authenticated:
        return redirect('home')
    
    match_pk = request.POST.get("match_pk")
    roll_no = request.POST.get("roll_no")
    team_num = int(request.POST.get("team_name"))
    amount = request.POST.get("amount")

    match = Match.objects.get(match_pk=match_pk)
    teams = [match.team1.name, match.team2.name]
    team_name = teams[team_num-1]


    bet = {
        "roll_no":roll_no,
        "team_name":team_name,
        "amount":amount,
        "match_pk":match_pk
    }

    return render(request, 'confirm.html',{
        "bet" : bet
    })