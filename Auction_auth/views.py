from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.messages.views import SuccessMessageMixin

# Create your views here.
from Auction_auth.forms import *


class HomePageView(TemplateView):
    template_name = "frontend/index.html"


class DashboardPageView(TemplateView):
    template_name = "backend/dashboard.html"


class LoginPageView(TemplateView):
    template_name = "backend/auth/login.html"


class RegisterPageView(SuccessMessageMixin, CreateView):
    model = User
    form_class = AccountCreationForm
    template_name = "backend/auth/register.html"
    success_message = "Registration Successful you can now login"

    def get_success_url(self):
        return reverse("auth:login")
