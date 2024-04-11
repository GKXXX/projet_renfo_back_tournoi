from django.test import TestCase, Client
from .models import Player, Tournament, Team, Match
from django.urls import reverse
import json

class PlayerTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_player_sign_up(self):
        response = self.client.post('/player-sign-up/', {'firstName': 'John', 'lastName': 'Doe'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['message'], 'Sign up done.')

    def test_player_sign_up_missing_data(self):
        response = self.client.post('/player-sign-up/', {'firstName': 'John'})
        self.assertEqual(response.status_code, 500)
        data = json.loads(response.content)
        self.assertEqual(data['message'], 'Some fields are lacking data.')

class TeamTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_team_show_match(self):
        team = Team.objects.create(name='Team 1')
        response = self.client.get(reverse('team_show_match', args=(team.id,)))
        self.assertEqual(response.status_code, 404)  # No matches available initially

class TournamentTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_tournament_show_match(self):
        tournament = Tournament.objects.create(name='Tournament 1')
        response = self.client.get(reverse('tournament_show_match', args=(tournament.id,)))
        self.assertEqual(response.status_code, 404)  # No matches available initially

    # Add more test cases for other endpoints related to tournaments

class MatchTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    # Add test cases for match-related endpoints

class AssignPlayerToTeamTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.player = Player.objects.create(firstName='John', lastName='Doe')
        self.team = Team.objects.create(name='Team 1')

    def test_assign_player_to_team(self):
        response = self.client.post(reverse('assign_player_to_team', args=(self.player.id, self.team.id)))
        self.assertEqual(response.status_code, 200)

    def test_assign_player_to_team_invalid_player(self):
        response = self.client.post(reverse('assign_player_to_team', args=(999, self.team.id)))
        self.assertEqual(response.status_code, 404)

    def test_assign_player_to_team_invalid_team(self):
        response = self.client.post(reverse('assign_player_to_team', args=(self.player.id, 999)))
        self.assertEqual(response.status_code, 404)

class AssignTeamToTournamentTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.player = Player.objects.create(firstName='John', lastName='Doe', is_capitaine=True)
        self.team = Team.objects.create(name='Team 1')
        self.tournament = Tournament.objects.create(name='Tournament 1')

    def test_assign_team_to_tournament(self):
        response = self.client.post(reverse('assign_team_to_tournament', args=(self.player.id, self.team.id, self.tournament.id)))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.team, self.tournament.teams.all())

    def test_assign_team_to_tournament_invalid_player(self):
        response = self.client.post(reverse('assign_team_to_tournament', args=(999, self.team.id, self.tournament.id)))
        self.assertEqual(response.status_code, 404)

    def test_assign_team_to_tournament_invalid_team(self):
        response = self.client.post(reverse('assign_team_to_tournament', args=(self.player.id, 999, self.tournament.id)))
        self.assertEqual(response.status_code, 404)

    def test_assign_team_to_tournament_invalid_tournament(self):
        response = self.client.post(reverse('assign_team_to_tournament', args=(self.player.id, self.team.id, 999)))
        self.assertEqual(response.status_code, 404)

class MatchResultTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.match = Match.objects.create()
        self.team = Team.objects.create(name='Team 1')

    def test_match_result(self):
        response = self.client.post(reverse('match_result', args=(self.match.id, self.team.id)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.match.winner, self.team)

    def test_match_result_invalid_match(self):
        response = self.client.post(reverse('match_result', args=(999, self.team.id)))
        self.assertEqual(response.status_code, 404)

    def test_match_result_invalid_team(self):
        response = self.client.post(reverse('match_result', args=(self.match.id, 999)))
        self.assertEqual(response.status_code, 404)

class MatchInfoTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.tournament = Tournament.objects.create(name='Tournament 1')
        self.team1 = Team.objects.create(name='Team 1')
        self.team2 = Team.objects.create(name='Team 2')
        self.match = Match.objects.create(tournament=self.tournament)
        self.match.teams.add(self.team1, self.team2)

    def test_match_info(self):
        response = self.client.get(reverse('match_info', args=(self.match.id,)))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('equipes', data)
        self.assertIn('tournament', data)
        self.assertIn('winner', data)

    def test_match_info_invalid_match(self):
        response = self.client.get(reverse('match_info', args=(999,)))
        self.assertEqual(response.status_code, 404)

class TournamentWinningMatchTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.tournament = Tournament.objects.create(name='Tournament 1')
        self.team = Team.objects.create(name='Team 1')
        self.match = Match.objects.create(tournament=self.tournament)
        self.match.teams.add(self.team)

    def test_tournament_winning_match(self):
        response = self.client.post(reverse('tournament_winning_match', args=(self.match.id,)))
        self.assertEqual(response.status_code, 200)
        self.tournament.refresh_from_db()
        self.assertEqual(self.tournament.winner, self.team)

    def test_tournament_winning_match_invalid_match(self):
        response = self.client.post(reverse('tournament_winning_match', args=(999,)))
        self.assertEqual(response.status_code, 404)

class TournamentDetailsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.tournament = Tournament.objects.create(name='Tournament 1', description='Description 1')

    def test_tournament_details(self):
        response = self.client.get(reverse('tournament_details', args=(self.tournament.id,)))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('name', data)
        self.assertIn('description', data)
        self.assertIn('winner', data)

    def test_tournament_details_invalid_tournament(self):
        response = self.client.get(reverse('tournament_details', args=(999,)))
        self.assertEqual(response.status_code, 404)

class PlayerUpdateTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.player = Player.objects.create(firstName='John', lastName='Doe')

    def test_player_update(self):
      data = {'firstName': 'Jane'}
      url = reverse('player_update',args=(self.player.id,))
      response = self.client.post(url, data=data)
      self.assertEqual(response.status_code, 200)
      self.player.refresh_from_db()
      self.assertEqual(self.player.firstName, 'Jane')

    def test_player_update_invalid_player(self):
        response = self.client.post(reverse('player_update', args=(999,)))
        self.assertEqual(response.status_code, 404)

class TournamentCreateTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_tournament_create(self):
        data = {'name': 'New Tournament', 'description': 'Description of the new tournament'}
        response = self.client.post(reverse('tournament_create'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Tournament.objects.filter(name='New Tournament').exists())

class TeamCreateTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_team_create(self):
        data = {'name': 'New Team'}
        response = self.client.post(reverse('team_create'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Team.objects.filter(name='New Team').exists())
