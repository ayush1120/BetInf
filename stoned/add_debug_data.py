# from django.core.management import setup_environ
# setup_environ(settings)

import os
import shutil
import random
import django
from django.db import models

random.seed(69)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stoned.settings")
django.setup()

from stoned import settings
from boobi.models import *
from django.contrib.auth.models import User, Group

teams = ["Battle Hawks",
 "Renegades", 
 "Defenders",
 "Spartans",
 "Vipers",
 "Phoenix",
 "Dementors",
 "Vikings"]

team_images = {"Battle Hawks" : os.path.join("team_logos", "Battle_Hawk.png"),
 "Renegades" : os.path.join("team_logos", "Renegades.png"), 
 "Defenders" : os.path.join("team_logos", "Defenders.png"),
 "Spartans" : os.path.join("team_logos", "Spartans.png"),
 "Vipers" : os.path.join("team_logos", "Vipers.png"),
 "Phoenix" : os.path.join("team_logos", "Phoenix.png"),
 "Dementors" : os.path.join("team_logos", "Dementors.png"),
 "Vikings" : os.path.join("team_logos", "Vikings.png")
 }

sports = ["Badminton", "Tennis", "Basketball"]

def add_data():
    serial=1
    User.objects.create_superuser('ayush', 'ayush@iitbhilai.ac.in', 'ayush')
    User.objects.create_user('mml', 'mml@boobi.com', 'mml123')
    User.objects.create_user('sukhiya', 'sukhiya@boobi.com', 'sukhiya123')
    User.objects.create_user('ankit', 'ankit@boobi.com', 'ankit123')

    bookie, _ = Group.objects.get_or_create(name="Bookie")
    scout, _ = Group.objects.get_or_create(name="Scout")
    healer, _ = Group.objects.get_or_create(name="Healer") 
    

    mml = User.objects.get(username="mml")
    sukhiya = User.objects.get(username="sukhiya")
    ankit = User.objects.get(username="ankit")

    mml.groups.add(Group.objects.get(name="Bookie"))
    mml.save()

    sukhiya.groups.add(Group.objects.get(name="Scout"))
    sukhiya.save()

    ankit.groups.add(Group.objects.get(name="Healer"))
    ankit.save()

    # print("\n\nmml groups : ", mml.groups)
    # sukhiya.groups.add(scout)
    # sukhiya.save()
    
    
    # scout.user_game.add(sukhiya)
    # scout.save()
    # bookie.user_game.add(mml)
    # bookie.save()
    
    for sport in sports:
        a = Sport()
        a.name = sport
        a.save()
    for team in teams:
        a = Team()
        a.name = team
        a.logo.name = team_images[team]
        # a.logo.path = os.path.join(settings.MEDIA_ROOT, a.logo.name)
        a.save()
    num_matches = random.randint(2, 5)
    num_game = 0
    my_matches = []
    my_betting_matches = []
    for i in range(num_matches):
        team1 = Team.objects.get(name=random.choice(teams))
        team2 = random.choice(teams)
        while team2==team1.name:
            team2 = random.choice(teams)
        team2 = Team.objects.get(name=team2)
        active = bool(random.randint(0, 1))
        if active==True:
            betting = bool(random.randint(0, 1))
        else:
            betting = False
        team1_amount = random.randint(300, 600)
        team2_amount = random.randint(300, 600)
        sport = Sport.objects.get(name=random.choice(sports))
        a = Match(team1=team1, team2=team2, team1_amount=team1_amount, team2_amount=team2_amount, active=active, betting_status=betting, sport=sport)
        a.save()
        match_pk = a.match_pk
        for i in range(num_game):
            mygame = Game()
            mygame.match = Match.objects.get(match_pk=match_pk)
            mygame.sport = Sport.objects.get(name="Badminton")
            mygame.team1 = Team.objects.get(name=mygame.match.team1.name)
            mygame.team2 = Team.objects.get(name=mygame.match.team2.name)
            mygame.save()

        my_matches.append(a)
        if a.betting_status==True:
            my_betting_matches.append(a)
    
    num_bets = random.randint(2, 5)
    if len(my_betting_matches)>0:
        for i in range(num_bets):
            match = random.choice(my_betting_matches)
            phone_no = random.randint(1174001, 1174120)*10
            match_teams = [match.team1, match.team2]
            team = match_teams[random.randint(0, 1)]
            amount = random.randint(10, 20)*5
            nick = "boobi.boona"
            curr_match = Match.objects.get(match_serial=match.match_serial, betting_status=True)
            bet = Bet(match=curr_match, phone_no=phone_no, team=team, amount=amount, nickname=nick)
            bet.save()

if __name__ == "__main__":
    BASE_DIR = settings.BASE_DIR
    if os.path.exists(os.path.join(settings.BASE_DIR, "db.sqlite3")):
        os.remove(os.path.join(settings.BASE_DIR, "db.sqlite3"))
    else:
        print("The file does not exist")
    
    if os.path.exists(os.path.join(BASE_DIR, "boobi", "migrations")):
        shutil.rmtree(os.path.join(BASE_DIR, "boobi", "migrations"))

    if os.path.exists(os.path.join(BASE_DIR, "stoned", "__pycache__")):
        shutil.rmtree(os.path.join(BASE_DIR, "stoned", "__pycache__"))
    
    if os.path.exists(os.path.join(BASE_DIR, "boobi", "__pycache__")):
        shutil.rmtree(os.path.join(BASE_DIR, "boobi", "__pycache__"))

    os.system("python manage.py makemigrations")
    os.system("python manage.py migrate --run-syncdb")
    add_data()