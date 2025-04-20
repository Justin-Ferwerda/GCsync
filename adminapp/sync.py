from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from environ import Env
from .models import ClassroomAssignment

env = Env()

def get_classroom_service_for_teacher(teacher):
    creds = Credentials(
        token=teacher.access_token,
        refresh_token=teacher.refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=env('GOOGLE_CLIENT_ID'),
        client_secret=env('GOOGLE_CLIENT_SECRET'),
        scopes=["https://www.googleapis.com/auth/classroom.coursework.students"]
    )
    return build('classroom', 'v1', credentials=creds)

def sync_classroom_assignments(teacher):
    service = get_classroom_service_for_teacher(teacher)
    total_synced = 0

    courses = service.courses().list(teacherId='me').execute().get('courses', [])
    for course in courses:
        course_id = course['id']
        coursework_items = service.courses().courseWork().list(courseId=course_id).execute().get('courseWork', [])

        for work in coursework_items:
            coursework_id = work['id']
            title = work['title']
            due_date = work.get('dueDate')
            scheduled_time = work.get('scheduledTime')

            due_date_obj = None
            if due_date:
                due_date_obj = f"{due_date['year']}-{due_date['month']:02d}-{due_date['day']:02d}"

            assignment, _ = ClassroomAssignment.objects.update_or_create(
                course_id=course_id,
                coursework_id=coursework_id,
                defaults={
                    'title': title,
                    'due_date': due_date_obj,
                    'scheduled_time': scheduled_time,
                }
            )

            assignment.teachers.add(teacher)
            total_synced += 1

    return total_synced
