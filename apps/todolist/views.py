from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import TaskList, Task, UserProfile, TaskHistory
from .forms import TaskListForm, TaskForm, CustomUserCreationForm, CustomAuthenticationForm, UserProfileForm
import csv

# Create your views here.

@login_required
def profile(request):
    task_lists = TaskList.objects.filter(user=request.user)
    
    # Configure pagination for task lists
    page = request.GET.get('task_lists_page', 1)
    task_lists_paginator = Paginator(task_lists, 10)  # 10 task lists per page
    
    try:
        task_lists = task_lists_paginator.page(page)
    except PageNotAnInteger:
        task_lists = task_lists_paginator.page(1)
    except EmptyPage:
        task_lists = task_lists_paginator.page(task_lists_paginator.num_pages)
    
    task_lists = TaskList.objects.filter(user=request.user)
    return render(request, 'todolist/profile.html', {'task_lists': task_lists})

@login_required
def create_task_list(request):
    if request.method == 'POST':
        form = TaskListForm(request.POST)
        if form.is_valid():
            task_list = form.save(commit=False)
            task_list.user = request.user
            task_list.save()
            return redirect('profile')
    else:
        form = TaskListForm()
    return render(request, 'todolist/create_task_list.html', {'form': form})

@login_required
def create_task(request, task_list_id):
    task_list = get_object_or_404(TaskList, pk=task_list_id)
    
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.task_list = task_list
            task.save()
            TaskHistory.objects.create(task=task, user=request.user, action='created')
            return redirect('task_list', task_list_id=task_list_id) 
    else:
        form = TaskForm()
    
    return render(request, 'todolist/create_task.html', {'form': form, 'task_list': task_list})

def user_register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('profile')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return render(request, 'registration/logout.html')

@login_required
def update_task_list(request, task_list_id):
    task_list = get_object_or_404(TaskList, pk=task_list_id, user=request.user)

    if request.method == 'POST':
        form = TaskListForm(request.POST, instance=task_list)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = TaskListForm(instance=task_list)

    return render(request, 'todolist/update_task_list.html', {'form': form, 'task_list': task_list})

@login_required
def delete_task_list(request, task_list_id):
    task_list = get_object_or_404(TaskList, pk=task_list_id, user=request.user)

    if request.method == 'POST':
        task_list.delete()
        return redirect('profile')

    return render(request, 'todolist/delete_task_list.html', {'task_list': task_list})

@login_required
def update_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task_list = task.task_list
    if task_list.user != request.user:
        return redirect('profile')  # Redirect unauthorized access

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list', task_list_id=task_list.id)
    else:
        form = TaskForm(instance=task)

    return render(request, 'todolist/update_task.html', {'form': form, 'task': task})

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task_list = task.task_list
    if task_list.user != request.user:
        return redirect('profile')  # Redirect unauthorized access

    if request.method == 'POST':
        task.delete()
        return redirect('task_list', task_list_id=task_list.id)

    return render(request, 'todolist/delete_task.html', {'task': task})

@login_required
def mark_done(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task_list = task.task_list
    if task_list.user != request.user:
        return redirect('profile')  # Redirect unauthorized access

    if not task.done:
        task.mark_done()
    else:
        task.mark_undone()

    return redirect('task_list', task_list_id=task_list.id)

@login_required
def search_tasks(request):
    query = request.GET.get('q', '')

    if query:
        tasks = Task.objects.filter(
            Q(description__icontains=query),
            task_list__user=request.user
        )
    else:
        tasks = Task.objects.none()

    return render(request, 'todolist/search_tasks.html', {'tasks': tasks, 'query': query})

@login_required
def export_task_lists(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="task_lists.csv"'

    writer = csv.writer(response)
    writer.writerow(['Task List', 'Task Description', 'Task Status'])

    task_lists = TaskList.objects.filter(user=request.user)

    for task_list in task_lists:
        tasks = task_list.task_set.all()
        for task in tasks:
            writer.writerow([task_list.name, task.description, 'Done' if task.done else 'Not Done'])

    return response

@login_required
def edit_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'todolist/edit_profile.html', {'form': form})

@login_required
def task_list(request, task_list_id):
    task_list = get_object_or_404(TaskList, pk=task_list_id, user=request.user)
    tasks = Task.objects.filter(task_list=task_list)
    return render(request, 'todolist/task_list.html', {'task_list': task_list, 'tasks': tasks})
