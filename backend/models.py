from django.db import models

# Create your models here.

class Team(models.Model):
    name = models.CharField(default="team", max_length=55)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }

class Player(models.Model):
    firstName = models.CharField(max_length=55)
    lastName = models.CharField(max_length=55)
    team = models.ForeignKey(Team, on_delete=models.CASCADE,null=True) 
    is_capitaine = models.BooleanField(null=True)

    def serialize(self):
        return {
            'id': self.id,
            'first_name': self.firstName,
            'last_name': self.lastName,
            'team': self.team.serialize() if self.team else None,  
            'is_capitaine': self.is_capitaine,
        }

class Tournament(models.Model):
    name = models.CharField(max_length=70)
    description = models.CharField(max_length=255,null=True)
    winner = models.ForeignKey(Team, on_delete=models.CASCADE,null=True)  
    teams = models.ManyToManyField(Team, related_name="tournaments",blank=True)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'winner': self.winner.serialize() if self.winner else None, 
            'teams': [team.serialize() for team in self.teams.all()],  
        }

class Match(models.Model):
    teams = models.ManyToManyField(Team, related_name="matchs")
    tournament = models.ForeignKey(Tournament,null=True, on_delete=models.CASCADE)  
    winner = models.ForeignKey(Team, on_delete=models.CASCADE,null=True)  

    def serialize(self):
        return {
            'id': self.id,
            'teams': [team.serialize() for team in self.teams.all()],
            'winner': self.winner.serialize() if self.winner else None,  
        }
