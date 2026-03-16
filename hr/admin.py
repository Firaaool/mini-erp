# hr/admin.py
from django.contrib import admin
from .models import Department, Position, Employee

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'headcount', 'manager']
    search_fields = ['name', 'code']

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ['title', 'department', 'level', 'min_salary', 'max_salary']
    list_filter = ['department', 'level']

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'full_name', 'department', 'position', 'status', 'leave_balance']
    list_filter = ['department', 'status', 'employment_type']
    search_fields = ['employee_id', 'first_name', 'last_name', 'email']