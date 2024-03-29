from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect, Http404, HttpResponse
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
import stripe
# stripe.api_key = "sk_test_51L5Xs6GCAqCizi1RncjTC84yc0J7jaecLFB5gj07ZDNWCREFyEylsunXTltlQleL3lWzEcLsqIFCInvn6wGYu2Xa00cIHRZjMz"
stripe.api_key = "sk_test_51N3J38JRcgaZzMZKtuOJjMLXMMpKNqcKfdaKDtlPfYLHIpKNnMAVg1gxyHf15ImRFZyVficIsw4JhI9jQs5lOpyP00Sr3TtdN5"


class HomePageView(TemplateView):
    template_name = "frontend/index.html"


class DashboardPageView(LoginRequiredMixin, TemplateView):
    template_name = "backend/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["furniture"] = Furniture.objects.all().count()
        context["biders"] = User.objects.filter(is_staff=False).count()
        context["on_going"] = len(
            [on_going for on_going in Furniture.objects.all() if timezone.now() >= on_going.start_date_and_time and timezone.now() < on_going.end_date_and_time])
        context["closed"] = len(
            [on_going for on_going in Furniture.objects.all() if timezone.now() > on_going.end_date_and_time])
        if not self.request.user.is_staff:
            context["won"] = Furniture.objects.filter(
                sold_to=self.request.user).count()
        return context


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
    success_message = "Product uploaded successfully! "

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = 'Create'
        return context

    def get_success_url(self):
        return reverse("auth:create_product")


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
        return reverse("auth:manage_product")


class DeleteFurnitureView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Furniture
    success_message = 'Product Deleted Successfully!'
    success_url = reverse_lazy('auth:manage_product')


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


def is_over(product_id):
    now = timezone.now()
    end_date_and_time = Furniture.objects.get(
        product_id=product_id).end_date_and_time
    if now > end_date_and_time:
        return True
    return False


def declare_winner(product_id):
    try:
        product = Furniture.objects.get(product_id=product_id)
        price = 0
        winner = ''

        all_bids = Bidding.objects.filter(product=product)

        for bid in all_bids:
            if bid.bid_price > price:
                winner = bid.bider
                price = bid.bid_price

        product.sold_to = winner
        product.sold_price = price
        product.save()
        return True
    except Furniture.DoesNotExist:
        return False


class OnGoingAuctionView(LoginRequiredMixin, ListView):
    template_name = "backend/auction/on_going.html"

    def get_queryset(self):
        all_furniture = Furniture.objects.all().order_by('-created')
        now = timezone.now()
        return [on_going for on_going in all_furniture if now >= on_going.start_date_and_time and now < on_going.end_date_and_time]


class ClosedAuctionView(LoginRequiredMixin, ListView):
    template_name = "backend/auction/closed.html"

    def get_queryset(self):
        all_furniture = Furniture.objects.all().order_by('-created')
        now = timezone.now()
        return [closed for closed in all_furniture if now > closed.end_date_and_time]


class BiddingDetailView(LoginRequiredMixin, View):
    def get(self, request, product_id):

        context = {
            "form": BiddingForm(product_id=product_id),
            "biders": Bidding.objects.filter(
                product=Furniture.objects.get(product_id=product_id)).order_by('-bid_date'),
        }

        try:
            is_completed = is_over(product_id)

            furniture = Furniture.objects.get(product_id=product_id)
            context["object"] = furniture
            context["is_over"] = is_completed

            if is_completed:
                # Award winner
                declare_winner(product_id)

                if request.htmx:

                    # End polling
                    return HttpResponse(status=200, headers={'HX-Redirect': reverse('auth:winner', args=[product_id])})

                return redirect('auth:winner', product_id)
            else:
                if request.htmx:
                    return render(request, 'partials/bider_list.html', context)

                return render(request, 'backend/auction/bid.html', context)

        except Furniture.DoesNotExist:
            messages.error(request, "Unable to get furniture!")
        return redirect('auth:on_going')

    def post(self, request, product_id):
        form = BiddingForm(
            request.POST, product_id=product_id)
        context = {
            "biders": Bidding.objects.filter(
                product=Furniture.objects.get(product_id=product_id)).order_by('-bid_date'),
        }
        furniture = Furniture.objects.get(product_id=product_id)
        is_completed = is_over(product_id)

        context["object"] = furniture
        context["is_over"] = is_completed

        if not is_completed:

            if form.is_valid():

                form = form.save(commit=False)
                form.product = Furniture.objects.get(
                    product_id=product_id)
                form.bider = request.user
                form.save()

                messages.success(request, 'You have successfully placed a bid')
                return redirect('auth:bid', product_id)
            else:
                messages.error(request, form.errors.as_text())

            context["form"] = form

            return render(request, 'backend/auction/bid.html', context)
        else:
            messages.error(
                request, "Bid session over, you can no longer place bid")
            return redirect('auth:bid', product_id)


class BidWinnerView(LoginRequiredMixin, View):
    def get(self, request, product_id):
        try:
            furniture = Furniture.objects.get(product_id=product_id)
            # if furniture has no buyer
            if not furniture.sold_to:
                biddings = Bidding.objects.filter(product=furniture).exists()
                # check if furniture has any bidding list
                if biddings:
                    declare_winner(product_id)
                    product = Furniture.objects.get(
                        product_id=product_id)
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

        return [furniture for furniture in Furniture.objects.all() if furniture.sold_to]


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


class DeleteWinView(SuccessMessageMixin, LoginRequiredMixin, View):

    def post(self, *args, **kwargs):
        product_id = self.kwargs['pk']
        furniture = Furniture.objects.get(product_id=product_id)
        furniture.sold_to = None
        furniture.sold_price = None

        furniture.save()
        messages.success(self.request, 'Winner has been deleted Successfully!')
        return redirect('auth:winners_list')


class MakePaymentView(View, LoginRequiredMixin):
    def get(self, request, product_id):
        obj = Furniture.objects.get(product_id=product_id)
        context = {
            'object': obj,
        }

        return render(request, 'backend/payment/make_payment.html', context)

    def post(self, request, product_id):

        obj = Furniture.objects.get(product_id=product_id)
        source = request.POST.get('stripeToken')

        try:
            customer = stripe.Customer.create(
                name=f'{request.user.name}',
                description=f'{obj.product_name}',
                source=source
            )

            charge = stripe.Charge.create(
                customer=customer,
                amount=round(obj.sold_price) * 100,
                currency='NGN',
                description=f'Payment for {obj.product_name}',
            )

            obj.is_sold = True
            obj.save()

            messages.success(
                request, ('Product will be delivered to your address!, kindly make sure you update your profile'))
            return redirect('auth:dashboard')

        except stripe.error.CardError:
            messages.error(request, ('Your card has insufficient funds!!'))

        return redirect('auth:make_payment', product_id)
