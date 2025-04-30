# views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from services import ClassroomService

@login_required
def classroom_assignments_view(request):
    assignments_by_course = ClassroomService(request.user).get_assignments_by_course()

    return render(request, 'assignments.html', {
        'assignments_by_course': assignments_by_course
    })
