from apps.account.models import User, UserBankAccount
from apps.wallet.models import WalletModel
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, *args, **kwargs):
    if created:
        UserBankAccount.objects.create(user=instance)


@receiver(post_save, sender=User)
def create_user_wallet(sender, instance, created, **kwargs):
    if created:
        WalletModel.objects.create(user=instance)
