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
    path('auth/manage_bidders', ManageBiddersPageView.as_view(),
         name='manage_bidders'),
    path('auth/delete_bidder/<str:pk>',
         DeleteBidderView.as_view(), name='delete_bidder'),
    path('auth/update_bidder/<str:pk>',
         EditBidderView.as_view(), name='update_bidder'),

    path('auth/create_furniture', CreateFurniturePageView.as_view(),
         name='create_furniture'),
    path('auth/manage_furniture', ManageFurniturePageView.as_view(),
         name='manage_furniture'),
    path('auth/update_furniture/<str:pk>',
         EditFurnitureView.as_view(), name='update_furniture'),
    path('auth/delete_furniture/<str:pk>',
         DeleteFurnitureView.as_view(), name='delete_furniture'),

    path('auth/create_admin', CreateAdminPageView.as_view(), name='create_admin'),
    path('auth/manage_admin', ManageAdminPageView.as_view(), name='manage_admin'),
    path('auth/update_admin/<str:pk>',
         EditAdminView.as_view(), name='update_admin'),
    path('auth/delete_admin/<str:pk>',
         DeleteAdminView.as_view(), name='delete_admin'),

    path('auth/on_going', OnGoingAuctionView.as_view(), name='on_going'),
    path('auth/closed', ClosedAuctionView.as_view(), name='closed'),
    path('auth/winner/<str:furniture_id>',
         BidWinnerView.as_view(), name='winner'),
    path('auth/winners_list', ManageAuctionWinnersView.as_view(), name='winners_list'),
    path('auth/bid/<str:furniture_id>', BiddingDetailView.as_view(), name='bid'),

    path('auth/profile/<str:pk>',
         UpdateProfileView.as_view(), name='profile'),
]
