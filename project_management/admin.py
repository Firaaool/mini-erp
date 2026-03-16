# project_management/admin.py
from django.contrib import admin
from .models import Project, ProjectMember, Task, TaskComment

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'status', 'priority', 'completion_percentage']
    list_filter = ['status', 'priority']

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'project', 'assigned_to', 'status', 'priority', 'due_date']
    list_filter = ['status', 'priority', 'project']

# Register the rest (optional for now)
admin.site.register(ProjectMember)
admin.site.register(TaskComment)