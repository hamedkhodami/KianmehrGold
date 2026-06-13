from apps.wallet.models import WithdrawRequestModel
from django import forms
from django.utils.translation import gettext_lazy as _


class WithdrawRequestForm(forms.ModelForm):
    class Meta:
        model = WithdrawRequestModel
        fields = ["amount"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

        self.fields["amount"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "مبلغ برداشت",
                "id": "withdraw-amount",
                "name": "amount",
            }
        )

    def clean_amount(self):
        amount = self.cleaned_data["amount"]

        if amount <= 0:
            raise forms.ValidationError(_("The amount must be greater than zero."))

        if amount > self.user.wallet.balance:
            raise forms.ValidationError(_("There are not enough wallet balances."))

        return amount
