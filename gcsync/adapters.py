from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class AutoLinkSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        if request.user.is_authenticated:
            sociallogin.connect(request, request.user)

            if sociallogin.account.provider == 'google':
                request.user.is_synced = True
                request.user.save()
