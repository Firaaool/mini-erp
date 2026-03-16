from rest_framework import serializers
from .models import LeaveType, LeaveRequest
from hr.models import Employee

class LeaveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveType
        fields = '__all__'
        read_only_fields = ['id', 'created_at']

class LeaveRequestSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(read_only=True ,source='employee.full_name')
    leave_type_name = serializers.ReadOnlyField(source='leave_type.name')
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = LeaveRequest
        fields = [
            'id', 'employee', 'employee_name', 'leave_type', 'leave_type_name',
            'start_date', 'end_date', 'total_days', 'reason', 'status', 
            'status_display', 'reviewed_by', 'reviewed_at', 'review_comment', 
            'attachment', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id','employee', 'total_days', 'status', 'reviewed_by',
            'reviewed_at', 'created_at', 'updated_at'
        ]

    def validate(self, attrs):
        if attrs['start_date'] > attrs['end_date']:
            raise serializers.ValidationError("End date cannot be before start date.")
        return attrs