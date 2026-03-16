from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from datetime import date
from hr.models import Department, Position, Employee
from leave_management.models import LeaveType, LeaveRequest
from attendance.models import AttendanceRecord
from project_management.models import Project


class AuthenticationTestCase(APITestCase):
    """Tests for user registration and login endpoints."""

    def test_user_registration_success(self):
        payload = {
            'username': 'johndoe',
            'email': 'john@company.com',
            'password': 'StrongPass123!',
            'password_confirm': 'StrongPass123!'
        }
        response = self.client.post('/api/auth/register/', payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        self.assertTrue(User.objects.filter(username='johndoe').exists())

    def test_login_success(self):
        User.objects.create_user(username='testuser', password='TestPass123!')
        payload = {'username': 'testuser', 'password': 'TestPass123!'}
        response = self.client.post('/api/auth/login/', payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)


class EmployeeTestCase(APITestCase):
    """Tests for the HR Employee API."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='admin', password='admin123', is_staff=True
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        self.dept = Department.objects.create(name='Engineering', code='ENG')
        self.pos = Position.objects.create(
            title='Backend Developer',
            department=self.dept,
            level='MID',
            min_salary=3000,
            max_salary=6000
        )

    def test_create_employee(self):
        payload = {
            'user': self.user.id,
            'first_name': 'Alice',
            'last_name': 'Smith',
            'email': 'alice@company.com',
            'department': self.dept.pk,
            'position': self.pos.pk,
            'hire_date': str(date.today()),
            'employment_type': 'FULL_TIME'
        }
        response = self.client.post('/api/employees/', payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class LeaveRequestTestCase(APITestCase):
    """Tests for Leave Management API."""

    def setUp(self):
        self.user = User.objects.create_user(username='emp_leave', password='pass123')
        self.emp = Employee.objects.create(
            user=self.user, first_name='Bob', last_name='Jones',
            email='bob@co.com', hire_date=date.today()
        )
        self.ltype = LeaveType.objects.create(name='Annual Leave', code='AL', max_days_per_year=21)
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_apply_for_leave(self):
        payload = {
            'leave_type': self.ltype.pk,
            'start_date': '2025-08-01',
            'end_date': '2025-08-05',
            'reason': 'Family vacation.'
        }
        response = self.client.post('/api/leaves/', payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(LeaveRequest.objects.first().status, 'PENDING')
