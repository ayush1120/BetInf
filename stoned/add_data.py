
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
    User.objects.create_superuser('ayush', 'ayush@iitbhilai.ac.in', 'lol123lol')

    scout, _ = Group.objects.get_or_create(name="Scout")
    bookie, _ = Group.objects.get_or_create(name="Bookie")
    healer, _ = Group.objects.get_or_create(name="Healer") 


    User.objects.create_user('scout1', 'scout1@iitbhilai.ac.in','78524862')
    scout1 = User.objects.get(username="scout1")
    User.objects.create_user('scout2', 'scout2@iitbhilai.ac.in','34512452')
    scout2 = User.objects.get(username="scout2")
    User.objects.create_user('scout3', 'scout3@iitbhilai.ac.in','24848445')
    scout3 = User.objects.get(username="scout3")
    User.objects.create_user('bookie1', 'bookie1@iitbhilai.ac.in','46899152')
    bookie1 = User.objects.get(username="bookie1")
    User.objects.create_user('bookie2', 'bookie2@iitbhilai.ac.in','61531235')
    bookie2 = User.objects.get(username="bookie2")
    User.objects.create_user('healer1', 'healer1@iitbhilai.ac.in','14565162')
    healer1= User.objects.get(username="healer1")
    User.objects.create_user('healer2', 'healer2@iitbhilai.ac.in','14435162')
    healer2 = User.objects.get(username="healer2")
    User.objects.create_user('mml', 'mml@iitbhilai.ac.in','dhkru9bzieh')
    mml = User.objects.get(username="mml")
    
    
    
    scout1.groups.add(Group.objects.get(name="Scout"))
    scout2.groups.add(Group.objects.get(name="Scout"))
    scout3.groups.add(Group.objects.get(name="Scout"))
    bookie1.groups.add(Group.objects.get(name="Bookie"))
    bookie2.groups.add(Group.objects.get(name="Bookie"))
    healer1.groups.add(Group.objects.get(name="Healer"))
    healer2.groups.add(Group.objects.get(name="Healer"))
    mml.groups.add(Group.objects.get(name="Healer"))
    mml.groups.add(Group.objects.get(name="Bookie"))

    

    # bookie, _ = Group.objects.get_or_create(name="Bookie") 
    # sukhiya = User.objects.get(username="sukhiya")


    # mml.groups.add(Group.objects.get(name="Bookie"))
    # mml.save()

    # sukhiya.groups.add(Group.objects.get(name="Scout"))
    # sukhiya.save()
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
