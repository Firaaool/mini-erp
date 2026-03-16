# attendance/admin.py
from django.contrib import admin
from .models import AttendanceRecord

@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ['employee', 'date', 'status', 'check_in', 'check_out', 'working_hours']
    list_filter = ['status', 'date']
    search_fields = ['employee__employee_id']