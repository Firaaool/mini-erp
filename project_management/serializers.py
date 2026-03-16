from rest_framework import serializers
from .models import Project, ProjectMember, Task, TaskComment


class ProjectSerializer(serializers.ModelSerializer):
    completion_percentage = serializers.FloatField(read_only=True)
    remaining_budget = serializers.DecimalField(max_digits=14, decimal_places=2,read_only=True)
    manager_name = serializers.CharField(source='project_manager.full_name', read_only=True)

    class Meta:
        model = Project
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    assignee_name = serializers.CharField(read_only=True ,source='assigned_to.full_name')
    project_code = serializers.CharField(source='project.code', read_only=True)

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['completed_at']


class ProjectMemberSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.full_name', read_only=True)

    class Meta:
        model = ProjectMember
        fields = '__all__'