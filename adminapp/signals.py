# classroom/signals.py
from allauth.socialaccount.signals import social_account_added
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Teacher
from .sync import sync_classroom_assignments
from allauth.socialaccount.models import SocialToken

@receiver(social_account_added)
def create_teacher_and_sync(sender, request, sociallogin, **kwargs):
    user = sociallogin.user

    # Get token details
    try:
        token = SocialToken.objects.get(account__user=user)
    except SocialToken.DoesNotExist:
        return  # Token hasn't been saved yet

    teacher, created = Teacher.objects.get_or_create(
        user=user,
        defaults={
            'google_id': sociallogin.account.uid,
            'access_token': token.token,
            'refresh_token': token.token_secret or '',
            'token_expiry': token.expires_at,
        }
    )

    if not created:
        # Update token info if already exists
        teacher.access_token = token.token
        teacher.refresh_token = token.token_secret or ''
        teacher.token_expiry = token.expires_at
        teacher.save()

    # Sync assignments from Classroom
    sync_classroom_assignments(teacher)
