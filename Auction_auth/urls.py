from django.urls import path

from Auction_auth.views import *

app_name = "auth"

urlpatterns = [
    path('', HomePageView.as_view(), name='home')
]
