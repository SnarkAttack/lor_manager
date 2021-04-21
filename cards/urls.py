from django.urls import path
from .views import CardIndexView

urlpatterns = [
    path('', CardIndexView.as_view(), name='card_index'),
]