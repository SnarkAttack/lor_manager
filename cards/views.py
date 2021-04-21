from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import render
from .models import Card

class CardIndexView(TemplateView):

    def get(self, request, *args, **kwargs):
        ownable_cards = Card.objects.filter(collectible=True).order_by('-supertype', 'cost', 'name')
        ownable_card_img_abspaths = [[c.get_img_abspath() for c in ownable_cards[i*4:(i+1)*4]] for i in range(int(len(ownable_cards)/4)+1)]
        context = {'img_paths': ownable_card_img_abspaths}
        return render(request, 'cards/card_index.html', context)