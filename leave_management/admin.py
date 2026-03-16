# leave_management/admin.py
from django.contrib import admin
from .models import LeaveType, LeaveRequest

@admin.register(LeaveType)
class LeaveTypeAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'max_days_per_year', 'is_paid', 'requires_approval']

@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ['employee', 'leave_type', 'start_date', 'total_days', 'status', 'reviewed_by']
    list_filter = ['status', 'leave_type']
    search_fields = ['employee__first_name', 'reason']