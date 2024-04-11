from django.shortcuts import render,get_object_or_404
from .models import Player,Tournament,Team,Match
from django.http import JsonResponse
import random

# Create your views here.

def get_matches_by_team_id(team_id):
    try:
        matches = Match.objects.filter(teams__id=team_id)
        return matches
    except Match.DoesNotExist:
        return None


def PlayerSignUp(request):
  if ('lastName' in request.POST) and ('firstName' in request.POST) and (request.POST['firstName']) and (request.POST['lastName']):
    player = Player(firstName=request.POST.get('firstName'),lastName=request.POST.get('lastName'))
    player.save()
    data = {"message":"Sign up done."}
    return JsonResponse(data,status=200)
  else:
    data = {"message":"Some fields are lacking data."}
    return JsonResponse(data,status=500)
  
def TeamShowMatch(request,idTeam):
  try:
    matchs = Match.objects.filter(teams__id=idTeam)
    if len(matchs) > 0:
      data ={"matchs": [match.serialize() for match in matchs]}
      return JsonResponse(data,status=200)
    else :
      return JsonResponse({"error": "Not found"}, status=404)
  except:
    return JsonResponse({"error": "Not found"}, status=404)
  
def TournamentShowMatch(request,idTournament):
  try:
    matchs = Match.objects.filter(tournament=idTournament)
    if len(matchs) > 0:
      data ={"matchs": [match.serialize() for match in matchs]}
      return JsonResponse(data,status=200)
    else :
      return JsonResponse({"error": "Not found"}, status=404)
  except:
    return JsonResponse({"error": "Not found"}, status=404)
  
def AssignPlayerToTeam(request,idPlayer,IdTeam):
  try:
    player = get_object_or_404(pk=idPlayer,klass=Player)
    player.team = get_object_or_404(pk=IdTeam,klass=Team)
    player.save()
    data={"message":"Player updated successfully"}
    return JsonResponse(data,status=200)
  except:
    return JsonResponse({"error": "Not found"}, status=404)
  
def AssignTeamToTournament(request,idPlayer,idTeam,idTournament):
  try:
    player = get_object_or_404(pk=idPlayer,klass=Player)
    if player.is_capitaine:
      team = get_object_or_404(pk=idTeam,klass=Team)
      tournament = get_object_or_404(pk=idTournament,klass=Tournament)
      tournament.teams.add(team)
      tournament.save()
      data = {"message":"Team successfully added to the tournament."}
      return JsonResponse(data,status=200)
    else:
      data = {"message":"You are not the captain, you can't sign up your team to this tournament."}
      return JsonResponse(data,status=500)
  except:
    return JsonResponse({"error": "Not found"}, status=404)
  
def MatchResult(request,idMatch,idWinner):
  try: 
    match = get_object_or_404(pk=idMatch,klass=Match)
    match.winner = idWinner
    match.save()
    data={"message":"Winner successfully added."}
    return JsonResponse(data,status=200)
  except:
    return JsonResponse({"error": "Not found"}, status=404)
  
def MatchInfo(request,idMatch):
  try:
    match = get_object_or_404(pk=idMatch,klass=Match)
    tournament = get_object_or_404(pk=match.tournament,klass=Tournament)
    serialized_object = {
      "equipes":match.teams,
      "tournament":{
        "name":tournament.name
      },
      "winner":match.winner
    }
    return JsonResponse(serialized_object)
  except:
    return JsonResponse({"error": "Not found"}, status=404)

def TournamentWinningMatch(request,idMatch):
  try:
    match = get_object_or_404(pk=idMatch,klass=Match)
    tournament = get_object_or_404(pk=match.tournament,klass=Tournament)
    tournament.winner = match.winner
    tournament.save()
    data = {"message":"Winner has been chosen."}
    return JsonResponse(data,status=200)
  except:
    data={"message":"Tournament wasn't found."}
    return JsonResponse({"error": "Not found"}, status=404)

def TournamentDetails(request,idTournament):
  try:
    tournament = get_object_or_404(pk=idTournament,klass=Tournament)
    serialized_object = {
      "name":tournament.name,
      "description":tournament.description,
      "winner":tournament.winner
    }
    return JsonResponse(serialized_object)
  except:
    return JsonResponse({"error": "Not found"}, status=404)
  
def PlayerUpdate(request,idPlayer):
  try:
    player = get_object_or_404(pk=idPlayer,klass=Player)
    if request.POST['firstName'] != None:
      player.firstName = request.firstName
    if request.POST['lastName'] != None:
      player.lastName = request.lastName
    player.save()
    data = {
      "message":"Player updated succesfully."
    }
    return JsonResponse(data,status=200)
  except:
    return JsonResponse({"error": "Not found"}, status=404)
  
def TournamentCreate(request):
  tournament = Tournament(name=request.POST['name'],description=request.POST['description'])
  tournament.save()
  data = {
    "message":"Tournament created succesfully"
  }
  return JsonResponse(data,status=200)

def TeamCreate(request):
  team = Team(name=request.POST['name'])
  team.save()
  data = {
    "message":"Team created succesfully"
  }
  return JsonResponse(data,status=200)

def create_random_matches(request,idTournament):
  tournament = get_object_or_404(pk=idTournament,klass=Tournament)
  teams = tournament.teams.all()
  team_list = list(teams)
  random.shuffle(team_list)

  matches = []

  for i in range(0, len(team_list), 2):
    if i + 1 < len(team_list):
      match = Match.objects.create(tournament=tournament, team1=team_list[i], team2=team_list[i + 1])
      matches.append(match)

  return matches