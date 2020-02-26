from django.db import models
from boobi.includes.bett import water_down, get_odds
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
    name = models.CharField(max_length=25)
    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=25)
    logo = models.FileField(verbose_name="Team Logo", upload_to="team_logos/")

    def __str__(self):
        return self.name 


class Match(models.Model):
    match_pk = models.IntegerField(primary_key=True, auto_created=True)
    match_id = models.CharField(editable=True, max_length=25)
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team1")
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team2")
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now=True)
    team1_amount = models.FloatField(verbose_name="Amount Bet for Team 1", default=500)
    team2_amount = models.FloatField(verbose_name="Amount Bet for Team 2", default=500)
    team1_score = models.IntegerField(verbose_name="Team 1 Score", default=0)
    team2_score = models.IntegerField(verbose_name="Team 2 Score", default=0)

    def __str__(self):
        return self.match_id
    @property
    def get_multipliers(self):
        """
            returns [team1 multiplier, team2 multiplier]
        """
        multipliers = get_odds(self.team1_amount, self.team2_amount)
        return multipliers

    def save(self, *args, **kwargs):
        self.match_id = str(self.match_pk) + "__" +  teams_abbrv[self.team1.name] + "__" + teams_abbrv[self.team2.name] 
        super().save(*args, **kwargs)
    # team1_bet_amount

class Bet(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    bet_id = models.AutoField(primary_key=True)
    roll_no = models.BigIntegerField(default=0)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
    multiplier = models.FloatField(default=1)

    
    def __str__(self):
        return str(self.bet_id)

    def place_bet(self):
        """
            Places Bet, Updates Multipliers or Amount Placed per Team
        """
        team1 = self.match.team1.name
        team2 = self.match.team2.name

        team = self.team.name
        multipliers = get_odds(self.match.team1_amount, self.match.team2_amount)
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
            


