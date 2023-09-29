from django.test import TestCase
from django.contrib.auth.models import User
from .models import TaskList, Task

# Create your tests here.

class TaskListTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.task_list = TaskList.objects.create(name='Test List', user=self.user)
        self.task = Task.objects.create(task_list=self.task_list, description='Test Task')

    def test_task_creation(self):
        self.assertEqual(self.task.description, 'Test Task')

    def test_task_list_creation(self):
        self.assertEqual(self.task_list.name, 'Test List')
        self.assertEqual(self.task_list.user, self.user)

class TaskTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.task_list = TaskList.objects.create(name='Test List', user=self.user)
        self.task = Task.objects.create(task_list=self.task_list, description='Test Task')

    def test_task_completion(self):
        self.task.done = True
        self.task.save()
        self.assertTrue(self.task.done)
        
class AuthenticationTests(TestCase):
    def test_user_registration(self):
        response = self.client.post('/register/', {'username': 'newuser', 'password1': 'password123', 'password2': 'password123'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_user_login(self):
        response = self.client.post('/login/', {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.client.login(username='testuser', password='testpassword'))
