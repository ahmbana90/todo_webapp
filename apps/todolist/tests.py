from django.test import TestCase
from django.contrib.auth.models import User
from .models import TaskList, Task
from .forms import TaskListForm
from django.urls import reverse

class ViewsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.task_list = TaskList.objects.create(user=self.user, name='Test Task List')

    def test_profile_view(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todolist/profile.html')

    def test_create_task_list_view(self):
        response = self.client.post(reverse('create_task_list'), {'name': 'New Task List'})
        self.assertEqual(response.status_code, 302)  # Redirects after successful form submission
        self.assertTrue(TaskList.objects.filter(user=self.user, name='New Task List').exists())
        
class ModelsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.task_list = TaskList.objects.create(user=self.user, name='Test Task List')

    def test_task_model(self):
        task = Task.objects.create(task_list=self.task_list, description='Test Task')
        self.assertEqual(str(task), 'Test Task')
        
class FormsTestCase(TestCase):
    def test_task_list_form_valid(self):
        form_data = {'name': 'New Task List'}
        form = TaskListForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_task_list_form_empty_name(self):
        form_data = {'name': ''}
        form = TaskListForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)