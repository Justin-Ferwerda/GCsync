from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from services import ClassroomService

@csrf_exempt  # Only if you want to test w/o CSRF — remove in production
@login_required
def bulk_update_assignments_view(request):
    if request.method == 'POST':
        service = ClassroomService(request.user)
        assignments_by_course = service.get_assignments_by_course()

        for assignments in assignments_by_course.values():
            for a in assignments:
                assignment_id = a['id']
                course_id = a['courseId']

                due_key = f'due_date_{assignment_id}'
                schedule_key = f'scheduled_date_{assignment_id}'

                due_date = request.POST.get(due_key)
                scheduled_date = request.POST.get(schedule_key)

                update_data = {}

                if due_date:
                    y, m, d = map(int, due_date.split('-'))
                    update_data['dueDate'] = {'year': y, 'month': m, 'day': d}

                if scheduled_date:
                    y, m, d = map(int, scheduled_date.split('-'))
                    update_data['scheduledDate'] = {'year': y, 'month': m, 'day': d}

                if update_data:
                    try:
                        service.courses().courseWork().patch(
                            courseId=course_id,
                            id=assignment_id,
                            body=update_data
                        ).execute()
                    except Exception as e:
                        print(f'Error updating assignment {assignment_id}: {e}')

        return redirect('classroom_assignments')

    return redirect('classroom_assignments')
