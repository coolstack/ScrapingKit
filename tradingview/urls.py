from django.urls import path,include
from . import views

app_name = 'tradingview'

urlpatterns = [
    path('<str:symbol>/<int:duration>/<int:num>/', views.targetscrape, name = 'target_scraping'),
]
