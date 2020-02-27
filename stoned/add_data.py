
# from django.core.management import setup_environ
# setup_environ(settings)

import os
import shutil
import random
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stoned.settings")
django.setup()

from stoned import settings
from boobi.models import *
from django.contrib.auth.models import User

teams = ["Battle Hawks",
 "Renegades", 
 "Defenders",
 "Spartans",
 "Vipers",
 "Phoenix",
 "Dementors",
 "Vikings"]

sports = ["Badminton", "Tennis", "Basketball"]

def add_data():
    serial=1
    User.objects.create_superuser('ayush', 'ayush@iitbhilai.ac.in', 'ayush')
    
    for sport in sports:
        a = Sport()
        a.name = sport
        a.save()
    for team in teams:
        a = Team()
        a.name = team
        a.save()
    num_matches = random.randint(2, 5)
    
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
        a = Match(team1=team1, team2=team2, team1_amount=team1_amount, match_serial=serial, team2_amount=team2_amount, active=active, betting_status=betting, sport=sport)
        serial += 1
        a.save()
        my_matches.append(a)
        if a.betting_status==True:
            my_betting_matches.append(a)
    
    num_bets = random.randint(2, 5)
    if len(my_betting_matches)>0:
        for i in range(num_bets):
            match = random.choice(my_betting_matches)
            roll_no = random.randint(1174001, 1174120)*10
            match_teams = [match.team1, match.team2]
            team = match_teams[random.randint(0, 1)]
            amount = random.randint(10, 20)*5
            curr_match = Match.objects.get(match_serial=match.match_serial, betting_status=True)
            bet = Bet(match=curr_match, roll_no=roll_no, team=team, amount=amount)
            bet.save()

if __name__ == "__main__":
    BASE_DIR = settings.BASE_DIR
    if os.path.exists(os.path.join(settings.BASE_DIR, "db.sqlite3")):
        os.remove(os.path.join(settings.BASE_DIR, "db.sqlite3"))
    else:
        print("The file does not exist")
    
    if os.path.exists(os.path.join(BASE_DIR, "stoned", "__pycache__")):
        shutil.rmtree(os.path.join(BASE_DIR, "stoned", "__pycache__"))
    
    if os.path.exists(os.path.join(BASE_DIR, "boobi", "__pycache__")):
        shutil.rmtree(os.path.join(BASE_DIR, "boobi", "__pycache__"))

    os.system("python manage.py makemigrations")
    os.system("python manage.py migrate --run-syncdb")
    add_data()
