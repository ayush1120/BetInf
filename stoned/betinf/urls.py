"""trial URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:

    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
#from rest_framework.urlpatterns import format_suffix_patterns
from betinf import views

from .views import *
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
 
urlpatterns = [
    path('bet', views.show_bet_form, name='bet'),
    path('confirm', views.show_confirm_form, name='confirm'),
    path('updateScores', views.updateMatch, name = "updateMatch"),
    path('signin', views.signIn, name= "signin"),
    path('signout', views.signOut, name= "signout"),
    path('loda', views.loda, name="loda"),
    path('placebet', views.place_bet, name="placebet"),
    path('addmatch', views.add_match, name="addmatch"),
    path('addgame', views.add_game, name='addgame'),
    path('addset', views.addSet, name='addset'),
    path('updatescores', views.updateScores, name='updatescores'),
    path('toogleBettingStatus', views.toogleMatchBettingStatus, name='toogleBettingStatus'),
    path('toogleMatchActiveStatus', views.toogleMatchActiveStatus, name='toogleMatchActiveStatus'),
    path('deleteSet', views.deleteSet, name='deleteSet'),
    path('deleteLastGame', views.deleteGame, name='deleteLastGame'),
    path('serveHealer', views.serve_healer, name='serveHealer'),
    path('avStatusToogle', views.toogleAVStatus, name='avStatusToogle'),
    path('healMatch', views.healMatch, name='healMatch'),
    path('', views.show_home, name = 'home'),
]

# urlpatterns += staticfiles_urlpatterns()
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)