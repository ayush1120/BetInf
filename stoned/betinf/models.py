from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from betinf.includes.bett import water_down, get_odds
from betinf.includes.dump_csv import dump_bet
import uuid
# Create your models here.

teams_abbrv = {
"Battle Hawks" : "BH",
 "Renegades" : "RG", 
 "Defenders" : "DF",
 "Spartans" : "SP",
 "Vipers" : "VP",
 "Phoenix" : "PX",
 "Dementors" : "DM",
 "Vikings" : "VK"
 }



class Sport(models.Model):
    name = models.CharField(max_length=25, unique=True)
    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=25, unique=True)
    logo = models.FileField(verbose_name="Team Logo", upload_to="team_logos/", null=True)

    def __str__(self):
        return self.name 


class Match(models.Model):
    match_pk = models.AutoField(primary_key=True, auto_created=True, editable=False)
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team1")
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team2")
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    team1_amount = models.FloatField(verbose_name="Amount Bet for Team 1", default=0.01)
    team2_amount = models.FloatField(verbose_name="Amount Bet for Team 2", default=0.01)
    winner = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="match_winner", blank=True, null=True)
    active = models.BooleanField(default=False)
    betting_status = models.BooleanField(default=False)
    ended = models.BooleanField(default=False)

    def __str__(self):
        kol = str(self.match_pk) + "__" +  teams_abbrv[self.team1.name] + "__" + teams_abbrv[self.team2.name]
        return kol
    

    @property
    def team1_score(self):
        games = Game.objects.all().filter(match=Match.objects.get(match_pk=self.match_pk))
        t1_score = 0
        for game in games:
            if game.team1_score > game.team2_score:
                t1_score += 1
        return t1_score


    @property
    def team2_score(self):
        games = Game.objects.all().filter(match=Match.objects.get(match_pk=self.match_pk))
        t2_score = 0
        for game in games:
            if game.team1_score < game.team2_score:
                t2_score += 1
        return t2_score


    @property
    def num_games(self):
        numg = len(list(Game.objects.all().filter(match=Match.objects.get(match_pk=self.match_pk))))
        return numg

    @property
    def get_multipliers(self):
        """
            returns [team1 multiplier, team2 multiplier]
        """
        multipliers = get_odds(self.team1_amount, self.team2_amount)
        return multipliers

    @property
    def profit(self):
        bets_team1 = Bet.objects.all().filter(match=Match.objects.get(match_pk=self.pk), team=Team.objects.get(name=self.team1.name)).exclude(nickname="betinf.boona")
        bets_team2 =  Bet.objects.all().filter(match=Match.objects.get(match_pk=self.pk), team=Team.objects.get(name=self.team2.name)).exclude(nickname="betinf.boona")
        # admin_bets_team1 = Bet.objects.all().filter(match=Match.objects.get(match_pk=self.pk), nickname="betinf.boona",  team=Team.objects.get(name=self.team1.name))
        # admin_bets_team2 = Bet.objects.all().filter(match=Match.objects.get(match_pk=self.pk), nickname="betinf.boona",  team=Team.objects.get(name=self.team2.name))
        # admin_team1_sum = 0
        # x=0
        # for bet in admin_bets_team1:
        #     admin_team1_sum += bet.amount
        # amount1 = self.team1_amount - admin_team1_sum
        # admin_team2_sum = 0
        # for bet in admin_bets_team2:
        #     admin_team2_sum += bet.amount
        # amount2 = self.team2_amount - admin_team2_sum
        payout_team1 = 0
        betamount_team1 = 0
        for bet in bets_team1:
            payout_team1 += round(bet.amount*bet.multiplier, 2)
            betamount_team1 += round(bet.amount, 2)
        
        payout_team2 = 0
        betamount_team2 = 0
        for bet in bets_team2:
            payout_team2 += round(bet.amount*bet.multiplier, 2)
            betamount_team2 += round(bet.amount, 2)
        
        profit1 = betamount_team1 + betamount_team2 - payout_team1
        profit2 = betamount_team1 + betamount_team2 - payout_team2

        return [profit1, profit2]


class Game(models.Model):
    game_pk =  models.AutoField(primary_key=True)
    datetime = models.DateTimeField(auto_now_add=True)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="game_team1")
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="game_team2")
    team1_score = models.IntegerField(verbose_name="Team 1 Score", default=0)
    team2_score = models.IntegerField(verbose_name="Team 2 Score", default=0)
    winner = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="game_winner", blank=True, null=True)
    active = models.BooleanField(default=False)
    game_num=models.IntegerField(blank=True, editable=False, default=0)
    
    @property
    def num_sets(self):
        mysets = Set.objects.all().filter(game=Game.objects.get(game_pk=self.pk))
        return len(mysets)

    @property
    def team1_score(self):
        sets = Set.objects.all().filter(game=Game.objects.get(game_pk=self.game_pk))
        t1_score = 0
        for myset in sets:
            if myset.team1_score > myset.team2_score:
                t1_score += 1
        return t1_score


    @property
    def team2_score(self):
        sets = Set.objects.all().filter(game=Game.objects.get(game_pk=self.game_pk))
        t2_score = 0
        for myset in sets:
            if myset.team1_score < myset.team2_score:
                t2_score += 1
        return t2_score

    def declare_winner(self):
        if self.team1_score>self.team2_score:
            self.winner = self.team1
        elif self.team1_score<self.team2_score:
            self.winner = self.team2
        self.save()

    def __str__(self):
        return (str(self.match) + "__Game__" +  str(self.game_num)) 

    
    def save(self, *args, **kwargs):
        prev_games = list(Game.objects.filter(match=Match.objects.get(match_pk=self.match.match_pk)))
        if not Game.objects.filter(game_pk=self.game_pk).exists():
            self.game_num =  len(prev_games)+1

        super().save(*args, **kwargs)


class Set(models.Model):
    set_pk =  models.AutoField(primary_key=True)
    datetime = models.DateTimeField(auto_now_add=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    team1_score = models.IntegerField(verbose_name="Team 1 Score", default=0)
    team2_score = models.IntegerField(verbose_name="Team 2 Score", default=0)
    ended = models.BooleanField(default=False)
    team1_wickets = models.IntegerField(default=0)
    team2_wickets = models.IntegerField(default=0)
    team1_overs = models.IntegerField(default=0)
    team2_overs = models.IntegerField(default=0)
    set_num=models.IntegerField(blank=True, editable=False)



    def __str___(self):
        return str(self.game) + "__Set__" + str(self.set_num)

    def save(self, *args, **kwargs):
        prev_sets = list(Set.objects.filter(game=Game.objects.get(game_pk=self.game.game_pk)))
        if not Set.objects.filter(set_pk=self.set_pk).exists():
            self.set_num =  len(prev_sets)+1
        super().save(*args, **kwargs)
        




class Bet(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    bet_id = models.AutoField(primary_key=True, editable=False)
    nickname = models.CharField(max_length=50, default='Unknown', blank=True)
    phone_no = models.BigIntegerField(default=0)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
    multiplier = models.FloatField(default=1, editable=False)
    datetime = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.bet_id)

    @property
    def payout(self):
        return round(self.amount*self.multiplier, 2)


    def place_bet(self):
        """
            Places Bet, Updates Multipliers or Amount Placed per Team
        """
        team1 = self.match.team1.name
        team2 = self.match.team2.name

        team = self.team.name
        multipliers = get_odds(self.match.team1_amount, self.match.team2_amount)
        print(self.amount, self.team.name)
        if team==team1:
            self.multiplier = multipliers[0]
            my_match = self.match
            my_match.team1_amount += self.amount
            my_match.save()
        elif team == team2:
            self.multiplier = multipliers[1]
            my_match = self.match
            my_match.team2_amount += self.amount
            my_match.save()
        else:
            self.multiplier = 1

        return self.multiplier
    
    def save(self, *args, **kwargs):
        self.place_bet()
        data = [str(self.phone_no), str(self.match.match_pk), str(self.match), str(self.team.name), str(self.amount), str(round(self.amount*self.multiplier,2))]
        dump_bet(data, self.match)
        super().save(*args, **kwargs)




class AdminBet(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    bet_id = models.AutoField(primary_key=True, editable=False)
    nickname = models.CharField(max_length=50, default='betinf.boona', blank=True)
    phone_no = models.BigIntegerField(default=9600000069)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
    datetime = models.DateTimeField(auto_now_add=True)
    multiplier = models.FloatField(default=1, editable=False)


    def place_bet(self):
        """
            Places Bet, Updates Multipliers or Amount Placed per Team
        """
        team1 = self.match.team1.name
        team2 = self.match.team2.name

        team = self.team.name
        multipliers = get_odds(self.match.team1_amount, self.match.team2_amount)
        print(self.amount, self.team.name)
        if team==team1:
            self.multiplier = multipliers[0]
            my_match = self.match
            my_match.team1_amount += self.amount
            my_match.save()
        elif team == team2:
            self.multiplier = multipliers[1]
            my_match = self.match
            my_match.team2_amount += self.amount
            my_match.save()
        else:
            self.multiplier = 1

        return self.multiplier

    def save(self, *args, **kwargs):
        self.place_bet()
        super().save(*args, **kwargs)

class AdminBetVapourizer(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)