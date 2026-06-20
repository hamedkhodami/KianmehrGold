import random
from random import randint

from apps.account import forms
from apps.account.mixins import LogoutRequiredMixin
from apps.account.models import User, UserBankAccount
from apps.account.services.otp_service import OTPService
from apps.core.utils import toast_form_errors
from apps.notification.enums import NotificationEnums
from apps.notification.models import Notification
from apps.wallet.models import WalletTransactionModel
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views import View
from django.views.generic import FormView


class RegisterView(LogoutRequiredMixin, FormView):
    template_name = "account/signup.html"
    form_class = forms.UserCreationForm
    success_url = reverse_lazy("account:send_code")

    def form_valid(self, form):
        user = form.save()

        otp_code = str(random.randint(100000, 999999))

        OTPService.set_otp(user.phone_number, otp_code)

        self.request.session["verify_user_id"] = str(user.id)

        Notification.objects.create(
            type=NotificationEnums.MOBILE_VERIFICATION_CODE,
            title=_("Verification Code"),
            kwargs={"code": otp_code},
            to_user=user,
        )

        return super().form_valid(form)

    def form_invalid(self, form):
        toast_form_errors(self.request, form)
        return super().form_invalid(form)


class LoginView(LogoutRequiredMixin, FormView):
    template_name = "account/login.html"
    form_class = forms.LoginForm
    success_url = "/"

    def remember_me(self, form):
        if not form.cleaned_data.get("remember_me"):
            self.request.session.set_expiry(0)
            self.request.session.modified = True

    def form_valid(self, form):
        user = form.cleaned_data["user"]

        if not user.is_verified:
            self.request.session["verify_user_id"] = user.id

            return redirect("account:send_code")

        login(self.request, user)
        self.remember_me(form)

        messages.success(self.request, _("Login successful"))

        return super().form_valid(form)

    def form_invalid(self, form):
        toast_form_errors(self.request, form)
        return super().form_invalid(form)


class SendCodeView(LogoutRequiredMixin, View):
    def get_redirect_url(self):
        return self.request.GET.get("next", reverse("account:verify_phone"))

    def get(self, request):
        user_id = request.session.get("verify_user_id")

        if not user_id:
            messages.error(request, _("Session expired. Please try again."))
            return redirect("account:register")

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            messages.error(request, _("There is an issue! please try again"))
            return redirect("account:register")

        if not OTPService.can_send(user.phone_number):
            messages.warning(request, _("Please wait before requesting another code."))

            return redirect(self.get_redirect_url())

        code = randint(100000, 999999)

        OTPService.set_otp(user.phone_number, str(code))

        Notification.objects.create(
            type=NotificationEnums.MOBILE_VERIFICATION_CODE.value,
            title=_("Phone number verification code"),
            kwargs={"code": code},
            to_user=user,
            send_notify=True,
        )

        messages.info(request, _("Code sent to you"))
        return redirect(self.get_redirect_url())


class VerifyPhoneNumberView(LogoutRequiredMixin, FormView):
    template_name = "account/verify_phone.html"
    form_class = forms.VerifyPhoneNumberForm
    success_url = reverse_lazy("public:home")

    def form_valid(self, form):
        code = form.cleaned_data["code"]
        user_id = self.request.session.get("verify_user_id")

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            messages.error(self.request, _("There is an issue! please try again"))
            return redirect("account:register")

        if not OTPService.verify_otp(user.phone_number, code):
            messages.error(self.request, _("Entered code is not correct"))
            return redirect("account:verify_phone")

        user.is_verified = True
        user.save()

        login(self.request, user)

        self.request.session.pop("verify_user_id", None)

        messages.success(self.request, _("Register done successful"))
        return redirect(self.success_url)

    def form_invalid(self, form):
        toast_form_errors(self.request, form)
        return super().form_invalid(form)


class GetPhoneNumberView(LogoutRequiredMixin, FormView):
    template_name = "account/password/get_phone.html"
    form_class = forms.GetPhoneNumberForm

    def get_success_url(self):
        return (
            reverse("account:send_code")
            + f'?next={reverse("account:reset_pass_confirm")}'
        )

    def form_valid(self, form):
        user = form.cleaned_data["user"]

        self.request.session["verify_user_id"] = user.id

        return super().form_valid(form)

    def form_invalid(self, form):
        toast_form_errors(self.request, form)
        return super().form_invalid(form)


class ResetPassConfirmView(LogoutRequiredMixin, FormView):
    template_name = "account/password/reset_pass_confirm.html"
    form_class = forms.VerifyPhoneNumberForm
    success_url = reverse_lazy("account:reset_pass_complete")

    def form_valid(self, form):
        code = form.cleaned_data["code"]

        user_id = self.request.session.get("verify_user_id")

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            messages.error(self.request, _("There is an issue! please try again"))
            return redirect("account:get_phone_number")

        if not OTPService.verify_otp(user.phone_number, code):
            messages.error(self.request, _("Entered code is not correct"))

            return redirect("account:reset_pass_confirm")

        self.request.session["reset_user_id"] = user.id

        return super().form_valid(form)

    def form_invalid(self, form):
        toast_form_errors(self.request, form)
        return super().form_invalid(form)


class ResetPassCompleteView(LogoutRequiredMixin, FormView):
    template_name = "account/password/reset_pass_complete.html"
    form_class = forms.ResetPassForm
    success_url = reverse_lazy("account:login")

    def form_valid(self, form):
        password = form.cleaned_data.get("password2")
        user_id = self.request.session.get("reset_user_id")

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            messages.error(self.request, _("There is an issue! please try again"))
            return self.form_invalid(form)

        user.set_password(password)
        user.is_verified = True
        user.save()

        self.request.session.pop("reset_user_id", None)
        self.request.session.pop("verify_user_id", None)

        messages.success(self.request, _("Password successfully reset"))
        return super().form_valid(form)

    def form_invalid(self, form):
        toast_form_errors(self.request, form)
        return super().form_invalid(form)


class UserProfileView(LoginRequiredMixin, FormView):
    template_name = "account/profile.html"
    form_class = forms.UserProfileForm
    success_url = reverse_lazy("account:profile")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        messages.success(self.request, _("Profile updated successfully"))
        return super().form_valid(form)

    def form_invalid(self, form):
        toast_form_errors(self.request, form)
        return super().form_invalid(form)


class UserBankAccountView(LoginRequiredMixin, FormView):
    template_name = "account/bank_account.html"
    form_class = forms.UserBankAccountForm
    success_url = reverse_lazy("account:bank_account")

    def get_bank_account(self):
        bank_account = self.request.user.bank_accounts.first()
        if not bank_account:
            bank_account = UserBankAccount.objects.create(
                user=self.request.user, is_default=True
            )
        return bank_account

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = self.get_bank_account()
        return kwargs

    def form_valid(self, form):
        form.save()
        messages.success(self.request, _("Bank account updated successfully"))
        return super().form_valid(form)

    def form_invalid(self, form):
        toast_form_errors(self.request, form)
        return super().form_invalid(form)


class AdminUserDetailView(LoginRequiredMixin, View):
    def get(self, request, user_id):

        user = get_object_or_404(User, id=user_id)

        wallet = getattr(user, "wallet", None)
        gold_inventory = getattr(user, "gold_inventories", None)

        bank_accounts = user.bank_accounts.all()

        wallet_tx = WalletTransactionModel.objects.filter(wallet=wallet).order_by(
            "-created_at"
        )
        wallet_tx_page = Paginator(wallet_tx, 10).get_page(
            request.GET.get("wallet_page")
        )

        payments = user.payments.order_by("-created_at")
        payments_page = Paginator(payments, 10).get_page(
            request.GET.get("payment_page")
        )

        orders = user.orders.order_by("-created_at")
        orders_page = Paginator(orders, 10).get_page(request.GET.get("order_page"))

        withdraws = user.withdraw_requests.order_by("-created_at")
        withdraws_page = Paginator(withdraws, 10).get_page(
            request.GET.get("withdraw_page")
        )

        return render(
            request,
            "account/user_detail.html",
            {
                "user_obj": user,
                "wallet": wallet,
                "gold_inventory": gold_inventory,
                "bank_accounts": bank_accounts,
                "wallet_tx_page": wallet_tx_page,
                "payments_page": payments_page,
                "orders_page": orders_page,
                "withdraws_page": withdraws_page,
            },
        )
