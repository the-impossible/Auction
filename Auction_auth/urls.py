from django.urls import path

from Auction_auth.views import *

app_name = "auth"

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),

    path('auth/dashboard', DashboardPageView.as_view(), name='dashboard'),

    path('login', LoginPageView.as_view(), name='login'),
    path('register', RegisterPageView.as_view(), name='register'),
    path('logout', LogoutView.as_view(), name='logout'),

    path('auth/create_bidder', CreateBidderPageView.as_view(), name='create_bidder'),
    path('auth/manage_bidders', ManageBiddersPageView.as_view(), name='manage_bidders'),
    path('auth/delete_bidder/<str:pk>', DeleteBidderView.as_view(), name='delete_bidder'),
    path('auth/update_bidder/<str:pk>', EditBidderView.as_view(), name='update_bidder'),

    path('auth/create_furniture', CreateFurniturePageView.as_view(), name='create_furniture'),
    path('auth/manage_furniture', ManageFurniturePageView.as_view(), name='manage_furniture'),
    path('auth/update_furniture/<str:pk>', EditFurnitureView.as_view(), name='update_furniture'),
    path('auth/delete_furniture/<str:pk>', DeleteFurnitureView.as_view(), name='delete_furniture'),
]
