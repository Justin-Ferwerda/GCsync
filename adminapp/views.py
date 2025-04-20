# classroom/views.py

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from allauth.socialaccount.models import SocialAccount, SocialToken
from django.utils.timezone import now, timedelta
from .models import Teacher
from .sync import sync_classroom_assignments

@login_required
def sync_teacher_and_assignments(request):
    user = request.user

    try:
        teacher = user.teacher
    except Teacher.DoesNotExist:
        try:
            social = SocialAccount.objects.get(user=user, provider="google")
            token = SocialToken.objects.get(account=social)

            teacher = Teacher.objects.create(
                user=user,
                google_id=social.uid,
                access_token=token.token,
                refresh_token=token.token_secret,
                token_expiry=now() + timedelta(seconds=token.expires_at.timestamp() - now().timestamp() if token.expires_at else 3600),
            )
        except (SocialAccount.DoesNotExist, SocialToken.DoesNotExist):
            messages.error(request, "Google login info is missing. Please re-authenticate.")
            return redirect("/admin/")

    try:
        count = sync_classroom_assignments(teacher)
        messages.success(request, f"✅ Synced {count} assignments.")
    except Exception as e:
        messages.error(request, f"❌ Sync failed: {e}")

    return redirect("/admin/")
