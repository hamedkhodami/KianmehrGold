from django import forms

from apps.product.enums import CoinCategoryEnum
from apps.product.models import CoinModel


class CoinModelForm(forms.ModelForm):
    class Meta:
        model = CoinModel
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # BANK
        if self.instance and self.instance.pk:
            if self.instance.category == CoinCategoryEnum.BANK:
                self.fields["market_extra_fee"].widget.attrs["readonly"] = True
                self.fields["market_percent_fee"].widget.attrs["readonly"] = True

        # PARSIAN
        if self.instance and self.instance.pk:
            if self.instance.category == CoinCategoryEnum.PARSIAN:
                self.fields["coin_type"].widget.attrs["readonly"] = True
