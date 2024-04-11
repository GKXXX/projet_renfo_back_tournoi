from django.urls import path
from . import views

urlpatterns = [
    path('player/signup/', views.PlayerSignUp, name='player_signup'),
    path('team/<int:idTeam>/matches/', views.TeamShowMatch, name='team_show_match'),
    path('tournament/<int:idTournament>/matches/', views.TournamentShowMatch, name='tournament_show_match'),
    path('player/<int:idPlayer>/assign/<int:IdTeam>/', views.AssignPlayerToTeam, name='assign_player_to_team'),
    path('player/<int:idPlayer>/team/<int:idTeam>/tournament/<int:idTournament>/', views.AssignTeamToTournament, name='assign_team_to_tournament'),
    path('match/<int:idMatch>/result/<int:idWinner>/', views.MatchResult, name='match_result'),
    path('match/<int:idMatch>/', views.MatchInfo, name='match_info'),
    path('tournament/<int:idMatch>/winner/', views.TournamentWinningMatch, name='tournament_winning_match'),
    path('tournament/<int:idTournament>/', views.TournamentDetails, name='tournament_details'),
    path('player/update/<int:idPlayer>/', views.PlayerUpdate, name='player_update'),
    path('tournament/create/', views.TournamentCreate, name='tournament_create'),
    path('team/create/', views.TeamCreate, name='team_create'),
    path('tournament/<int:idTournament>/random/matches/', views.create_random_matches, name='create_random_matches'),
]
