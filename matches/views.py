from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from matches.models import Match, MatchPlayer
from lor_accounts.models import LorAccount


class MatchIndexView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):

        game_name = 'SnarkAttack'

        lor_account = LorAccount.objects.get(game_name=game_name)

        match_players = MatchPlayer.objects.filter(account__id=lor_account.id)

        matches = Match.objects.filter(game_mode="Constructed", game_type__in=['Normal', 'Ranked'], players__in=[p.id for p in match_players]).order_by('-game_start_time')

        matchups = []

        for match in matches:
            user_player = match.players.get(account=lor_account)
            opponent = match.players.all().exclude(account=lor_account)[0]

            matchups.append((user_player, opponent))

        context = {
            'matchups': matchups,
        }

        return render(request, 'matches/match_index.html', context)
