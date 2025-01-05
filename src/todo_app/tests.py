from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status
from datetime import datetime, timedelta
from .models import Todo

class TodoAPITest(TestCase):
    def setUp(self):
        # Create test users
        self.user1 = User.objects.create_user(
            username='testuser1',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            password='testpass123'
        )
        
        # Create API client
        self.client = APIClient()
        
        # Create some todos for testing
        self.todo1 = Todo.objects.create(
            title='Test Todo 1',
            description='Test Description 1',
            user=self.user1,
            priority=1
        )
        self.todo2 = Todo.objects.create(
            title='Test Todo 2',
            description='Test Description 2',
            user=self.user1,
            completed=True,
            priority=2
        )
        self.todo3 = Todo.objects.create(
            title='Test Todo 3',
            description='Test Description 3',
            user=self.user1,
            due_date=timezone.now() - timedelta(days=1),
            priority=3
        )

    def test_register_user(self):
        """Test user registration"""
        data = {
            'username': 'newuser',
            'password': 'newpass123',
            'email': 'new@example.com'
        }
        response = self.client.post('/api/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_user(self):
        """Test user login"""
        data = {
            'username': 'testuser1',
            'password': 'testpass123'
        }
        response = self.client.post('/api/login/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_create_todo(self):
        """Test creating a new todo"""
        self.client.force_authenticate(user=self.user1)
        data = {
            'title': 'New Todo',
            'description': 'New Description',
            'priority': 2,
            'due_date': timezone.now() + timedelta(days=1)
        }
        response = self.client.post('/api/todos/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Todo')

    def test_list_todos(self):
        """Test listing todos"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get('/api/todos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_todo_detail(self):
        """Test retrieving a specific todo"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(f'/api/todos/{self.todo1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Todo 1')

    def test_update_todo(self):
        """Test updating a todo"""
        self.client.force_authenticate(user=self.user1)
        data = {'title': 'Updated Todo'}
        response = self.client.patch(f'/api/todos/{self.todo1.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Todo')

    def test_delete_todo(self):
        """Test deleting a todo"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(f'/api/todos/{self.todo1.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Todo.objects.filter(id=self.todo1.id).exists())

    def test_todo_status(self):
        """Test todo status field"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(f'/api/todos/{self.todo2.id}/')
        self.assertEqual(response.data['status'], 'completed')
        
        response = self.client.get(f'/api/todos/{self.todo3.id}/')
        self.assertEqual(response.data['status'], 'overdue')

    def test_todo_statistics(self):
        """Test todo statistics endpoint"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get('/api/todos/statistics/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total'], 3)
        self.assertEqual(response.data['completed'], 1)
        self.assertEqual(response.data['pending'], 2)
        self.assertEqual(response.data['overdue'], 1)

    def test_clear_completed(self):
        """Test clearing completed todos"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete('/api/todos/clear_completed/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Todo.objects.filter(completed=True).exists())

    def test_user_isolation(self):
        """Test that users can only access their own todos"""
        self.client.force_authenticate(user=self.user2)
        response = self.client.get('/api/todos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

        response = self.client.get(f'/api/todos/{self.todo1.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
