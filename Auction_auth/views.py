from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.urls import reverse_lazy
from django.utils import timezone

# Create your views here.
from Auction_auth.forms import *
from Auction_auth.models import *


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


class EditFurnitureView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
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


class CreateAdminPageView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = User
    form_class = AdminCreationForm
    template_name = "backend/admin/create_update_admin.html"
    success_message = "Admin account created successfully! "

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = 'Create'
        return context

    def get_success_url(self):
        return reverse("auth:create_admin")

    def form_valid(self, form):
        form.instance.is_staff = True
        form = super().form_valid(form)

        return form


class ManageAdminPageView(LoginRequiredMixin, ListView):
    template_name = "backend/admin/manage_admin.html"

    def get_queryset(self):
        return User.objects.filter(is_staff=True, is_superuser=False).order_by('-date_joined')


class EditAdminView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = User
    template_name = "backend/admin/create_update_admin.html"
    form_class = UpdateAdminForm
    success_message = 'Admin Account Updated Successfully!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = 'Update'
        return context

    def get_success_url(self):
        return reverse("auth:manage_admin")


class DeleteAdminView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = User
    success_message = 'Admin Account Deleted Successfully!'
    success_url = reverse_lazy('auth:manage_admin')


def is_over(furniture_id):
    now = timezone.now()
    end_date_and_time = Furniture.objects.get(
        furniture_id=furniture_id).end_date_and_time
    if now > end_date_and_time:
        return True
    return False


def declare_winner(furniture_id):
    try:
        furniture = Furniture.objects.get(furniture_id=furniture_id)
        price = 0
        winner = ''

        all_bids = Bidding.objects.filter(furniture=furniture)

        for bid in all_bids:
            if bid.bid_price > price:
                winner = bid.bider
                price = bid.bid_price

        furniture.sold_to = winner
        furniture.sold_price = price
        furniture.save()
        return True
    except Furniture.DoesNotExist:
        return False


class OnGoingAuctionView(LoginRequiredMixin, ListView):
    template_name = "backend/auction/on_going.html"

    def get_queryset(self):
        all_furniture = Furniture.objects.all().order_by('-created')
        now = timezone.now()
        return [on_going for on_going in all_furniture if now < on_going.end_date_and_time]


class ClosedAuctionView(LoginRequiredMixin, ListView):
    template_name = "backend/auction/closed.html"

    def get_queryset(self):
        all_furniture = Furniture.objects.all().order_by('-created')
        now = timezone.now()
        return [closed for closed in all_furniture if now > closed.end_date_and_time]


class BiddingDetailView(LoginRequiredMixin, View):
    def get(self, request, furniture_id):

        context = {
            "form": BiddingForm(furniture_id=furniture_id),
            "biders": Bidding.objects.filter(
                furniture=Furniture.objects.get(furniture_id=furniture_id)).order_by('-bid_date'),
        }

        try:
            is_completed = is_over(furniture_id)

            furniture = Furniture.objects.get(furniture_id=furniture_id)
            context["object"] = furniture
            context["is_over"] = is_completed

            if is_completed:
                # Award winner
                declare_winner(furniture_id)

                if request.htmx:

                    # End polling
                    response['HX-Redirect'] = "true"
                    response = redirect('auth:winner', furniture_id)

                    return response

                return redirect('auth:winner', furniture_id)
            else:
                if request.htmx:
                    return render(request, 'partials/bider_list.html', context)

                return render(request, 'backend/auction/bid.html', context)

        except Furniture.DoesNotExist:
            messages.error(request, "Unable to get furniture!")
        return redirect('auth:on_going')

    def post(self, request, furniture_id):
        form = BiddingForm(
            request.POST, furniture_id=furniture_id)
        context = {
            "biders": Bidding.objects.filter(
                furniture=Furniture.objects.get(furniture_id=furniture_id)).order_by('-bid_date'),
        }
        furniture = Furniture.objects.get(furniture_id=furniture_id)
        is_completed = is_over(furniture_id)

        context["object"] = furniture
        context["is_over"] = is_completed

        if not is_completed:

            if form.is_valid():

                form = form.save(commit=False)
                form.furniture = Furniture.objects.get(
                    furniture_id=furniture_id)
                form.bider = request.user
                form.save()

                messages.success(request, 'You have successfully placed a bid')
                return redirect('auth:bid', furniture_id)
            else:
                messages.error(request, form.errors.as_text())

            context["form"] = form

            return render(request, 'backend/auction/bid.html', context)
        else:
            messages.error(
                request, "Bid session over, you can no longer place bid")
            return redirect('auth:bid', furniture_id)


class BidWinnerView(LoginRequiredMixin, View):
    def get(self, request, furniture_id):
        try:
            furniture = Furniture.objects.get(furniture_id=furniture_id)
            # if furniture has no buyer
            if not furniture.sold_to:
                biddings = Bidding.objects.filter(furniture=furniture).exists()
                # check if furniture has any bidding list
                if biddings:
                    declare_winner(furniture_id)
                    furniture = Furniture.objects.get(
                        furniture_id=furniture_id)
                    return render(request, 'backend/auction/winner.html', {'object': furniture})
                else:
                    messages.error(
                        request, 'No one bided for it so no winner!')
                    return redirect('auth:closed')
            return render(request, 'backend/auction/winner.html', {'object': furniture})
        except Furniture.DoesNotExist:
            messages.error(request, 'Failed to get furniture!')
            return redirect('auth:closed')


class ManageAuctionWinnersView(LoginRequiredMixin, ListView):
    template_name = "backend/auction/winners.html"

    def get_queryset(self):

        return Bidding.objects.all()


class UpdateProfileView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = User
    template_name = "backend/profile/profile.html"
    form_class = BiddersUpdateForm
    success_message = 'Account Updated Successfully!'

    def get_context_data(self, **kwargs):
        if self.request.user.is_staff:
            form_class = UpdateAdminForm
        context = super().get_context_data(**kwargs)
        context["type"] = 'Update'
        return context

    # def get_success_url(self):
    #     return reverse("auth:profile", f'{self.request.user.pk}')
