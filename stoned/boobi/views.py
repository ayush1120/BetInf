from django.shortcuts import render, redirect
# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404

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
    for match in matches:
        if match.team1.logo != :
            print(str(match.team1.logo.url))
            print(str(match.team1.logo.url))
    return render(request, 'index.html', {
        'matches' : matches,
        "MEDIA_URL" : MEDIA_URL
    })


def show_bet_form(request):
    if not request.user.is_authenticated:
        return redirect('home')
    
    return render(request, 'bet.html')