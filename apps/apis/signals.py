from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from .models import UserAccount

@receiver(user_signed_up)
def create_profile(user, **kwargs):
    UserAccount.objects.create(user=user, username=user.username, email=user.email)