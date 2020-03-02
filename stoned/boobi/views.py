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
from boobi.models import Match, Bet, Team, Game, Set, AdminBet
from boobi.includes.bett import water_down


@csrf_exempt
def show_home(request):
    matches = Match.objects.all()
    # for match in matches:
    #     if match.team1.logo != None:
    #         print(str(match.team1.logo.url))
    #         print(str(match.team1.logo.url))
    user_group = user_access_level(request)
    games = Game.objects.all().order_by('datetime')
    sets = Set.objects.all()

    return render(request, 'index.html', {
        'matches': matches,
        'games': games,
        'sets': sets,
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
            redirect('home')
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
    games = Game.objects.all().order_by('datetime')
    game_pk = int(request.POST.get("game_pk"))
    team_num = int(request.POST.get("team_num"))
    inc = int(request.POST.get("inc"))
    # print("match_pk : ", match_pk)
    # print("team_num : ", team_num)
    # print("inc : ", inc)
    curr_game = Game.objects.get(game_pk=game_pk)
    if team_num == 1:
        if inc == 1:
            curr_game.team1_score += 1
            curr_game.save()
        else:
            curr_game.team1_score -= 1
            curr_game.save()
    else:
        if inc == 1:
            curr_game.team2_score += 1
            curr_game.save()
        else:
            curr_game.team2_score -= 1
            curr_game.save()

    print("match : ")
    print("team1 : ", curr_game.team1_score)
    print("team2 : ", curr_game.team2_score)
    user_group = user_access_level(request)

    return redirect('home')
    # render(request, 'index.html', {
    #     'matches': matches,
    #     'games': games,
    #     'user_group': user_group,
    # })


@csrf_exempt
def place_bet(request):
    if not request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        match_pk = int(request.POST.get("match_pk"))
        phone_no = int(request.POST.get("phone_no"))
        nickname = request.POST.get("nickname")
        team_name = str(request.POST.get("team_name"))
        amount = int(request.POST.get("amount"))
        match = Match.objects.get(match_pk=match_pk)
        team = Team.objects.get(name=team_name)
        bet = Bet(match=match, nickname=nickname, phone_no=phone_no, team=team, amount=amount)
        bet.save()

    return redirect('home')


@csrf_exempt
def show_confirm_form(request):
    if not request.user.is_authenticated:
        return redirect('home')

    match_pk = int(request.POST.get("match_pk"))
    phone_no = int(request.POST.get("phone_no"))
    team_num = int(request.POST.get("team_name"))
    nickname = request.POST.get("nickname")
    amount = int(request.POST.get("amount"))

    match = Match.objects.get(match_pk=match_pk)
    teams = [match.team1.name, match.team2.name]
    team_name = teams[team_num-1]
    payout = round(match.get_multipliers[team_num-1]*amount, 2)
    bet = {
        "phone_no": phone_no,
        "team_name": team_name,
        "amount": amount,
        "match_pk": match_pk,
        "payout": payout,
        "nickname": nickname,
    }
    print("mybet  :  ", bet)
    return render(request, 'confirm.html', {
        "bet": bet
    })


@csrf_exempt
def user_access_level(request):
    out_dict = {"logged_in": False,
                "scout": False,
                "bookie": False,
                "healer": False,
                "admin": False
                }
    if not request.user.is_authenticated:
        return out_dict
    out_dict["logged_in"] = True
    if request.user.is_superuser:
        out_dict["scout"] = True
        out_dict["bookie"] = True
        out_dict["healer"] = True
        out_dict["admin"] = True
        return out_dict
    if request.user.groups.filter(name="Bookie").exists():
        out_dict["bookie"] = True
    if request.user.groups.filter(name="Scout").exists():
        out_dict["scout"] = True
    if request.user.groups.filter(name="Healer").exists():
        out_dict["healer"] = True
    return out_dict


@csrf_exempt
def add_match(request):
    if request.method == "POST":
        sport_name = request.POST.get('sport_name')
        team1_name = request.POST.get('team_name_1')
        team2_name = request.POST.get('team_name_2')
        amount_team1 = int(request.POST.get('team1_amount'))
        amount_team2 = int(request.POST.get('team2_amount'))
        new_match = Match()
        new_match.sport = Sport.objects.get(name=sport_name)
        new_match.team1 = Team.objects.get(name=team1_name)
        new_match.team2 = Team.objects.get(name=team2_name)
        active = True
        betting_status = True
        new_match.save()
        curr_match = Match.objects.get(match_pk=new_match.pk)
        nick = "boobi.boona"
        phone = 9600000069
        bet1 = AdminBet(match=curr_match, nickname=nick, phone_no=phone, team=Team.objects.get(name=team1_name), amount=amount_team1)
        bet1.save()
        bett2=AdminBet(match=curr_match, nickname=nick, phone_no=phone, team=Team.objects.get(name=team2_name), amount=amount_team2)
        bett2.save()
        return redirect('home')
    if user_access_level(request)['admin'] == False:
        return redirect('home')
    teams=Team.objects.all()
    sports=Sport.objects.all()
    return render(request, 'make_match.html', {
    "teams": teams,
    "sports": sports,
    })


@csrf_exempt
def add_game(request):
    matches=Match.objects.all()
    # for match in matches:
    #     if match.team1.logo != None:
    #         print(str(match.team1.logo.url))
    #         print(str(match.team1.logo.url))
    user_group=user_access_level(request)
    games=Game.objects.all().order_by('datetime')
    if user_access_level(request)['scout'] == False:
        return redirect('home')
    match=Match.objects.get(match_pk=int(request.POST.get('match_pk')))
    new_game=Game()
    new_game.match=match
    new_game.sport=Sport.objects.get(name=match.sport.name)
    new_game.team1=Team.objects.get(name=match.team1.name)
    new_game.team2=Team.objects.get(name=match.team2.name)
    new_game.save()
    return redirect('home')

def loda(request):
    lol=user_access_level(request)
    return JsonResponse(lol)




@csrf_exempt
def addSet(request):
    if not request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        game_pk = request.POST.get("game_pk")
        game = Game.objects.get(game_pk=game_pk)
        if len(Set.objects.all().filter(game=game))>0:
            old_set = Set.objects.get(game=game, set_num=game.num_sets)
            old_set.ended = True
            if(old_set.team1_score>old_set.team2_score):
                game.team1_score += 1
                game.save()
            elif(old_set.team1_score<old_set.team2_score):
                game.team2_score += 1
                game.save()


        myset = Set()  
        myset.game = Game.objects.get(game_pk=game_pk)
        myset.save()

        return redirect('home')
    return redirect('home')


def updateScores(request):
    if not request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        game_pk = request.POST.get("game_pk")
        team1_score = int(request.POST.get("team1_score"))
        team2_score = int(request.POST.get("team2_score"))
        game = Game.objects.get(game_pk=game_pk)
        myset = Set.objects.get(game=game, set_num=game.num_sets) 
        myset.team1_score = team1_score
        myset.team2_score = team2_score
        print("team2_score : ", team2_score)
        print("team1_score : ", team1_score)
        myset.save()

        return redirect('home')
    return redirect('home')


def toogleMatchBettingStatus(request):
    if not request.user.is_authenticated:
        return redirect('home')
    
    user_group = user_access_level(request)
    if user_group['admin'] or user_group['healer']:
        if request.method == 'POST':
            match_pk = request.POST.get('match_pk')
            match=Match.objects.get(match_pk=match_pk)
            match.betting_status = not match.betting_status
            match.save()
            return redirect('home')
    return redirect('home')

def toogleMatchActiveStatus(request):
    if not request.user.is_authenticated:
        return redirect('home')
    
    user_group = user_access_level(request)
    if user_group['admin'] or user_group['healer']:
        if request.method == 'POST':
            match_pk = request.POST.get('match_pk')
            match=Match.objects.get(match_pk=match_pk)
            match.active = not match.active
            match.save()
            return redirect('home')
    return redirect('home')


def deleteSet(request):
    if not request.user.is_authenticated:
        return redirect('home')
    user_group = user_access_level(request)
    if not user_group['scout']:
        return redirect('home')
    if request.method=='POST':
        game_pk = int(request.POST.get("game_pk"))
        game = Game.objects.get(game_pk=game_pk)
        myset = Set.objects.get(game=game, set_num=game.num_sets)
        myset.delete()
        if Set.objects.filter(game=game, set_num=game.num_sets).exists():
            old_set = Set.objects.get(game=game, set_num=game.num_sets)
            old_set.ended = False
            old_set.save()
            if(old_set.team1_score>old_set.team2_score):
                game.team1_score -= 1
                game.save()
            elif(old_set.team1_score<old_set.team2_score):
                game.team2_score -= 1
                game.save()
        
        return redirect('home')


def deleteGame(request):
    if not request.user.is_authenticated:
        return redirect('home')
    user_group = user_access_level(request)
    if not user_group['scout']:
        return redirect('home')
    if request.method=='POST':
        game_pk = int(request.POST.get("game_pk"))
        game = Game.objects.get(game_pk=game_pk)
        game.delete()
        
        return redirect('home')


def serve_healer(request):
    if not request.user.is_authenticated:
        return redirect('home')
    user_group = user_access_level(request)
    if not (user_group['healer'] or user_group['bookie']):
        return redirect('home')
    if request.method=='POST':
        match_pk = request.POST.get("match_pk")
        match = Match.objects.get(match_pk=match_pk)
        bets = Bet.objects.all().filter(match=match)
        team1 = Team.objects.get(name=match.team1.name)
        team2 = Team.objects.get(name=match.team2.name)
        bets_team1 = bets.filter(team=team1)
        bets_team2 = bets.filter(team=team2)
        profit = match.profit
        odds = match.get_multipliers
        bets_amount_team_1 = 0
        bets_amount_team_2 = 0
        for bet in bets_team1:
            bets_amount_team_1 += bet.amount
        for bet in bets_team2:
            bets_amount_team_2 += bet.amount
        admin_bets_team1 = AdminBet.objects.filter(match=match, team=team1)
        admin_bets_team2 = AdminBet.objects.filter(match=match, team=team2)
        admin_bets_amount_team_1 = 0
        admin_bets_amount_team_2 = 0
        for bet in admin_bets_team1:
            admin_bets_amount_team_1 += bet.amount
        for bet in admin_bets_team2:
            admin_bets_amount_team_2 += bet.amount


        return render(request, 'healer_page.html', {
            "profit":profit,
            "odds":odds,
            "bets_amount_team_1":bets_amount_team_1,
            "bets_amount_team_2":bets_amount_team_2,
            "admin_bets_amount_team_1":admin_bets_amount_team_1,
            "admin_bets_amount_team_2":admin_bets_amount_team_2,
            "match":match,
            "bets":bets,
        })