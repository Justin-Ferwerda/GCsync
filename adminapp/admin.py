from unfold.admin import ModelAdmin
from unfold.decorators import action
from django.contrib import admin
from django.shortcuts import redirect
from .models import ClassroomAssignment
from .sync import sync_classroom_assignments

@admin.register(ClassroomAssignment)
class ClassroomAssignmentAdmin(ModelAdmin):
    list_display = ("title", "due_date", "scheduled_time")
    
    def has_module_permission(self, request):
        return request.user.is_staff or hasattr(request.user, 'teacher')

    def has_view_permission(self, request, obj=None):
        return request.user.is_staff or hasattr(request.user, 'teacher')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        teacher = getattr(request.user, 'teacher', None)
        if teacher:
            return qs.filter(teachers=teacher)
        return qs.none()

    def changelist_view(self, request, extra_context=None):
        if 'sync' in request.GET:
            teacher = getattr(request.user, 'teacher', None)
            if teacher:
                count = sync_classroom_assignments(teacher)
                self.message_user(request, f"✅ Synced {count} assignments.")
            return redirect(request.path)
        return super().changelist_view(request, extra_context)

    @action(icon="fa ")
    def my_action(self, request, queryset):
        # Action logic here
        pass
