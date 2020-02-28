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
from boobi import views

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
    path('addset', views.add_set, name='addset'),
    path('', views.show_home, name = 'home'),
]

# urlpatterns += staticfiles_urlpatterns()
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)