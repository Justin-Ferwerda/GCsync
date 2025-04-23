from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from allauth.socialaccount.models import SocialToken
from environ import Env

class ClassroomService:

    def __init__(self, user):
        self.token = SocialToken.objects.get(account__user=user, account_provider='google')
        self.env = Env()
        self.credentials = self._get_credentials()
        self.service = build('classroom', 'v1', credentials=self.credentials)

    def _get_credentials(self):
        return Credentials(
            token = self.token.token,
            refresh_token = self.token.token_secret,
            token_uri = self.env('GOOGLE_TOKEN_URI'),
            client_id = self.env('GOOGLE_CLIENT_ID'),
            client_secret = self.env('GOOGLE_CLIENT_SECRET'),
            scopes = self.env.list('GOOGLE_CLIENT_SCOPES')
        )
    
    def list_courses(self):
        results = self.service.courses().list().execute()
        return results.get('courses', [])

    def list_assignments(self, course_id):
        results = self.service.courses().courseWork().list(courseId=course_id).execute()
        return results.get('courseWork', [])
