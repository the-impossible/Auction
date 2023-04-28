from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.urls import reverse_lazy

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
        messages.success(
            request, 'You are successfully logged out, to continue login again')
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
    template_name = "backend/bidders/create_update_bidder.html"
    success_message = "Registration Successful bidders can login to their account now! "

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = 'Create'
        return context

    def get_success_url(self):
        return reverse("auth:create_bidder")


class ManageBiddersPageView(LoginRequiredMixin, ListView):
    template_name = "backend/bidders/manage_bidders.html"

    def get_queryset(self):
        return User.objects.filter(is_staff=False, is_superuser=False).order_by('-date_joined')

class DeleteBidderView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = User
    success_message = 'Deleted Successfully!'
    success_url = reverse_lazy('auth:manage_bidders')

class EditBidderView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = User
    template_name = "backend/bidders/create_update_bidder.html"
    form_class = BiddersUpdateForm
    success_message = 'Updated Successfully!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = 'Update'
        return context

    def get_success_url(self):
        return reverse("auth:manage_bidders")

class CreateFurniturePageView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Furniture
    form_class = FurnitureForm
    template_name = "backend/furniture/create_update_furniture.html"
    success_message = "Furniture uploaded successfully! "

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = 'Create'
        return context

    def get_success_url(self):
        return reverse("auth:create_furniture")

class ManageFurniturePageView(LoginRequiredMixin, ListView):
    template_name = "backend/furniture/manage_furnitures.html"

    def get_queryset(self):
        return Furniture.objects.all().order_by('-created')

class EditFurnitureView(SuccessMessageMixin,LoginRequiredMixin, UpdateView):
    model = Furniture
    template_name = "backend/furniture/create_update_furniture.html"
    form_class = EditFurnitureForm
    success_message = 'Updated Successfully!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = 'Update'
        return context

    def get_success_url(self):
        return reverse("auth:manage_furniture")

class DeleteFurnitureView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Furniture
    success_message = 'Furniture Deleted Successfully!'
    success_url = reverse_lazy('auth:manage_furniture')