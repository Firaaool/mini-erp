from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import AttendanceRecord
from .serializers import AttendanceRecordSerializer

@extend_schema(tags=['Attendance Module'])
class AttendanceViewSet(viewsets.ModelViewSet):
    serializer_class = AttendanceRecordSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['date', 'status', 'location']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return AttendanceRecord.objects.all().select_related('employee')
        return AttendanceRecord.objects.filter(employee=user.employee_profile)

    @action(detail=False, methods=['post'], url_path='check-in')
    def check_in(self, request):
        """Record check-in for the current day."""
        employee = request.user.employee_profile
        today = timezone.now().date()

        if AttendanceRecord.objects.filter(employee=employee, date=today).exists():
            return Response({"detail": "Already checked in for today."}, status=status.HTTP_400_BAD_REQUEST)

        # Capture IP address for audit (per requirement on page 30)
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        ip = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')

        record = AttendanceRecord.objects.create(
            employee=employee,
            date=today,
            check_in=timezone.now(),
            location=request.data.get('location', 'OFFICE'),
            ip_address=ip
        )
        return Response(AttendanceRecordSerializer(record).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], url_path='check-out')
    def check_out(self, request):
        """Record check-out for the current day."""
        employee = request.user.employee_profile
        today = timezone.now().date()

        try:
            record = AttendanceRecord.objects.get(employee=employee, date=today)
            if record.check_out:
                return Response({"detail": "Already checked out today."}, status=status.HTTP_400_BAD_REQUEST)

            record.check_out = timezone.now()
            record.save()
            return Response(AttendanceRecordSerializer(record).data)
        except AttendanceRecord.DoesNotExist:
            return Response({"detail": "No check-in record found for today."}, status=status.HTTP_404_NOT_FOUND)