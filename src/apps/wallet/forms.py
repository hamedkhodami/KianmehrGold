from django import forms
from django.utils.translation import gettext_lazy as _

from apps.wallet.models import WithdrawRequestModel


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


class WalletChargeForm(forms.Form):

    amount = forms.IntegerField(min_value=10000, label="Amount")


class MeltedGoldBuyForm(forms.Form):
    amount = forms.DecimalField(
        label=_("Amount"),
        min_value=1000000,
        decimal_places=0,
        max_digits=18,
    )


class SellMeltedGoldForm(forms.Form):
    gold_amount = forms.DecimalField(
        label=_("Amount"),
        min_value=0.01,
        decimal_places=3,
        max_digits=18,
    )
