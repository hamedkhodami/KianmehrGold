from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from persian_tools import digits

from .models import User, UserBankAccount
from .utils import check_phone_number


class UserCreationForm(forms.ModelForm):
    phone_number = forms.CharField(label=_("Phone number"), max_length=11)
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password repeat"), widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("phone_number",)

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        phone_number = digits.convert_to_en(phone_number)

        if not check_phone_number(phone_number):
            raise ValidationError(_("Enter a valid phone number"))

        if User.objects.filter(phone_number=phone_number).exists():
            raise ValidationError(_("This phone number is already registered."))

        return phone_number

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError(_("Passwords are not match."))

        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    phone_number = forms.CharField(
        max_length=11,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": _("09__")}),
    )
    password = forms.CharField(
        max_length=128, required=True, widget=forms.PasswordInput()
    )
    remember_me = forms.BooleanField(
        required=False, widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )

    def clean(self):
        phone = self.cleaned_data.get("phone_number")
        password = self.cleaned_data.get("password")

        phone = digits.convert_to_en(phone)

        if not check_phone_number(phone):
            raise ValidationError(_("Enter a valid phone number"), code="BAD-PHONE")

        user = authenticate(username=phone, password=password)

        if not user:
            raise ValidationError(
                _("Phone number or password is incorrect"), code="INVALID-CREDENTIALS"
            )

        return {"user": user, "remember_me": self.cleaned_data.get("remember_me")}


class VerifyPhoneNumberForm(forms.Form):
    code = forms.CharField(max_length=6, required=True, widget=forms.NumberInput())

    def clean_code(self):
        code = self.cleaned_data.get("code")
        if not code.isdigit():
            raise ValidationError(_("Enter a valid code"))
        return code


class GetPhoneNumberForm(forms.Form):
    phone_number = forms.CharField(
        max_length=11, widget=forms.TextInput(attrs={"placeholder": "09__"})
    )

    def clean(self):
        cleaned_data = super().clean()

        phone_number = cleaned_data.get("phone_number")

        if not phone_number:
            return cleaned_data

        phone_number = digits.convert_to_en(phone_number)

        if not check_phone_number(phone_number):
            raise ValidationError(
                _("Enter a valid phone number"), code="BAD-PHONE-NUMBER"
            )

        try:
            user = User.objects.get(phone_number=phone_number)
        except (User.DoesNotExist, TypeError, KeyError) as err:
            raise ValidationError(_("No user found with this phone number")) from err

        cleaned_data["user"] = user

        return cleaned_data


class ResetPassForm(forms.Form):
    password = forms.CharField(
        max_length=128, min_length=4, required=True, widget=forms.PasswordInput()
    )
    password2 = forms.CharField(
        max_length=128, min_length=4, required=True, widget=forms.PasswordInput()
    )

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")

        if password and password2 and password != password2:
            raise ValidationError(_("Passwords are not match."))

        return password2


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "phone_number", "national_code", "email"]
        widgets = {
            "first_name": forms.TextInput(),
            "last_name": forms.TextInput(),
            "phone_number": forms.TextInput(),
            "national_code": forms.TextInput(),
            "email": forms.EmailInput(),
        }

    def clean_phone_number(self):
        phone = self.cleaned_data.get("phone_number")
        phone = digits.convert_to_en(phone)

        if not check_phone_number(phone):
            raise ValidationError(_("Enter a valid phone number"))

        # اگر شماره جدید است، باید unique باشد
        if (
            User.objects.filter(phone_number=phone)
            .exclude(id=self.instance.id)
            .exists()
        ):
            raise ValidationError(_("This phone number is already taken"))

        return phone

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if not email:
            return email

        if User.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise ValidationError(_("This email is already taken"))

        return email

    def clean_national_code(self):
        code = self.cleaned_data.get("national_code")
        if code and not code.isdigit():
            raise ValidationError(_("National code must be numeric"))
        if code and len(code) != 10:
            raise ValidationError(_("National code must be 10 digits"))
        return code


class UserBankAccountForm(forms.ModelForm):
    class Meta:
        model = UserBankAccount
        fields = ["bank_name", "card_number", "iban"]
        widgets = {
            "bank_name": forms.TextInput(),
            "card_number": forms.TextInput(),
            "iban": forms.TextInput(),
        }

    def clean_card_number(self):
        card = self.cleaned_data.get("card_number")
        if card:
            card = card.replace(" ", "").replace("-", "")
        return card

    def clean_iban(self):
        iban = self.cleaned_data.get("iban")
        if iban:
            iban = iban.replace(" ", "").upper()
        return iban
