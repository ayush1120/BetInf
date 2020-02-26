from django.shortcuts import render, redirect
# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404

from .models import *
import os
import shutil
import json
import datetime

import psutil
import signal
import random
import uuid
from stoned.settings import BASE_DIR, STATICFILES_DIRS

