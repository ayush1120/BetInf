from django.shortcuts import render, redirect
# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout


from .models import *
import os
import shutil
import json
import datetime

import signal
import random
import uuid
from stoned.settings import BASE_DIR, STATICFILES_DIRS, MEDIA_URL
from boobi.models import Match, Bet, Team
from boobi.includes.bett import water_down

@csrf_exempt
def show_home(request):
    matches = Match.objects.all()
    # for match in matches:
    #     if match.team1.logo != None:
    #         print(str(match.team1.logo.url))
    #         print(str(match.team1.logo.url))
    user_group = user_access_level(request)
    return render(request, 'index.html', {
        'matches': matches,
        'user_group': user_group
    })

@csrf_exempt
def show_bet_form(request):
    match_pk = request.POST.get("match_pk")
    match = Match.objects.get(match_pk=match_pk)
    if not request.user.is_authenticated:
        return redirect('home')
    user_group = user_access_level(request)
    return render(request, 'bet.html', {
        'match': match,
        'user_group': user_group
    })

@csrf_exempt
def signIn(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            matches = Match.objects.all()
            user_group = user_access_level(request)
            return render(request, 'index.html', {
                'matches': matches,
                'user_group': user_group
            })
        else:
            return redirect('signin')

    return render(request, 'signin.html')

def signOut(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('home')
    else:
        return redirect('home')

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
    if team_num == 1:
        if inc == 1:
            match.team1_score += 1
            match.save()
        else:
            match.team1_score -= 1
            match.save()
    else:
        if inc == 1:
            match.team2_score += 1
            match.save()
        else:
            match.team2_score -= 1
            match.save()

    print("match : ")
    print("team1 : ", match.team1_score)
    print("team2 : ", match.team2_score)
    user_group = user_access_level(request)

    return render(request, 'index.html', {
        'matches': matches,
        'user_group': user_group,
    })

@csrf_exempt
def show_confirm_form(request):
    if not request.user.is_authenticated:
        return redirect('home')

    if request.method=='POST':
        match_pk = int(request.POST.get("match_pk"))
        roll_no = int(request.POST.get("roll_no"))
        team_name = str(request.POST.get("team_name"))
        amount = int(request.POST.get("amount"))
        match = match.objects.get(match_pk=match_pk)
        team = Team.objects.get(name=team_name)
        bet = Bet(match=match, roll_no=roll_no, team=team, amount=amount)
        bet.save()

    match_pk = int(request.POST.get("match_pk"))
    roll_no = int(request.POST.get("roll_no"))
    team_num = int(request.POST.get("team_name"))
    amount = int(request.POST.get("amount"))

    match = Match.objects.get(match_pk=match_pk)
    teams = [match.team1.name, match.team2.name]
    team_name = teams[team_num-1]
    payout = round(match.get_multipliers[team_num-1]*amount, 2)
    bet = {
        "roll_no": roll_no,
        "team_name": team_name,
        "amount": amount,
        "match_pk": match_pk,
        "payout": payout,
    }

    return render(request, 'confirm.html', {
        "bet": bet
    })

@csrf_exempt
def user_access_level(request):
    out_dict = {"logged_in": False,
                "scout": False,
                "bookie": False,
                "admin": False
                }
    if not request.user.is_authenticated:
        return out_dict
    out_dict["logged_in"] = True
    if request.user.is_superuser:
        out_dict["scout"] = True
        out_dict["bookie"] = True
        out_dict["admin"] = True
        return out_dict
    if request.user.groups.filter(name="Bookie").exists():
        out_dict["bookie"] = True
    if request.user.groups.filter(name="Scout").exists():
        out_dict["scout"] = True
    return out_dict


def loda(request):
    lol = user_access_level(request)
    return JsonResponse(lol)
