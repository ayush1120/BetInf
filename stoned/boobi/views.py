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
from stoned.settings import BASE_DIR, STATICFILES_DIRS
from boobi.models import Match

def show_home(request):
    matches = Match.objects.all()
    return render(request, 'index.html', {
        'matches' : matches
    })


def show_bet_form(request):
    if not request.user.is_authenticated:
        return redirect('home')
    
    return render(request, 'bet.html')