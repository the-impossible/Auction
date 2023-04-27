from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

# Create your views here.
from Auction_auth.forms import *


class HomePageView(TemplateView):
    template_name = "frontend/index.html"

class DashboardPageView(LoginRequiredMixin, TemplateView):
    template_name = "backend/dashboard.html"

class LoginPageView(View):
    def get(self, request):
        return render(request, 'backend/auth/login.html')

    def post(self, request):
        email = request.POST.get('email').strip()
        password = request.POST.get('password').strip()

        if email and password:
            user = authenticate(request, email=email, password=password)

            if user:
                if user.is_active:
                    login(request, user)
                    messages.success(request, f"You are now signed in {user}")

                    nxt = request.GET.get('next', None)
                    if nxt is None:
                        return redirect('auth:dashboard')
                    return redirect(self.request.GET.get('next', None))

                else:
                    messages.warning(
                        request, 'Account not active contact the administrator')
            else:
                messages.error(request, 'Invalid login credentials')
        else:
            messages.error(request, 'All fields are required!!')

        return redirect('auth:login')

class LogoutView(LoginRequiredMixin, View):

    def post(self, request):
        logout(request)
        messages.success(request, 'You are successfully logged out, to continue login again')
        return redirect('auth:login')

class RegisterPageView(SuccessMessageMixin, CreateView):
    model = User
    form_class = AccountCreationForm
    template_name = "backend/auth/register.html"
    success_message = "Registration Successful you can now login"

    def get_success_url(self):
        return reverse("auth:login")

class CreateBidderPageView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = User
    form_class = BiddersCreationForm
    template_name = "backend/bidders/create_bidder.html"
    success_message = "Registration Successful bidders can login to their account now! "

    def get_success_url(self):
        return reverse("auth:create_bidder")
