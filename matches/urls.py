from django.urls import path
from .views import MatchIndexView

urlpatterns = [
    path('', MatchIndexView.as_view(), name='match_index'),
]