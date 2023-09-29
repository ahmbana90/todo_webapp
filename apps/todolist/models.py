from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class TaskList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

class Task(models.Model):
    task_list = models.ForeignKey(TaskList, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    done = models.BooleanField(default=False)
    deadline = models.DateTimeField(null=True, blank=True)
    priority = models.CharField(max_length=10, choices=[('high', 'High'), ('medium', 'Medium'), ('low', 'Low')], default='medium')

    def mark_done(self):
        self.done = True
        self.save()

    def mark_undone(self):
        self.done = False
        self.save()
    
    def __str__(self):
        return self.description
        
class SharedTaskList(models.Model):
    task_list = models.ForeignKey(TaskList, on_delete=models.CASCADE)
    shared_with = models.ForeignKey(User, on_delete=models.CASCADE)
    permission_level = models.CharField(max_length=10)
    
class UserFeedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    display_name = models.CharField(max_length=50, blank=True)
    bio = models.TextField(blank=True)


class TaskHistory(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=100)  # Action description (e.g., "created", "updated", "deleted")
    timestamp = models.DateTimeField(auto_now_add=True)