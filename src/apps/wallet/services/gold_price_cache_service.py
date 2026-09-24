from django.core.cache import cache

from apps.wallet.models import GoldPriceRuleModel


class MeltRuleCacheService:

    CACHE_KEY = "latest_melt_rule"

    @staticmethod
    def get_latest_rule():
        rule = cache.get(MeltRuleCacheService.CACHE_KEY)

        if rule is not None:
            return rule

        rule = (
            GoldPriceRuleModel.objects.filter(is_active=True)
            .order_by("-created_at")
            .first()
        )

        if rule is not None:
            cache.set(
                MeltRuleCacheService.CACHE_KEY,
                rule,
                10,
            )

        return rule
