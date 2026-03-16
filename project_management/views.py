from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Project, ProjectMember, Task
from .serializers import ProjectSerializer, ProjectMemberSerializer, TaskSerializer

@extend_schema(tags=['Project Management'])
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().select_related('project_manager')
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'code']

    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        """List team members for a specific project."""
        project = self.get_object()
        members = project.members.all().select_related('employee')
        serializer = ProjectMemberSerializer(members, many=True)
        return Response(serializer.data)

@extend_schema(tags=['Project Management'])
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().select_related('project', 'assigned_to')
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['project', 'status', 'priority', 'assigned_to']

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Mark a task as completed."""
        task = self.get_object()
        task.status = 'DONE'
        task.completed_at = timezone.now()
        task.save()
        return Response({'status': 'Task marked as done'})