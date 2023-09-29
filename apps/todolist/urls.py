from django.urls import path
from . import views

urlpatterns = [
    path('accounts/profile/', views.profile, name='profile'),
    path('register/', views.user_register, name='register'),
    path('create_task_list/', views.create_task_list, name='create_task_list'),
    path('create_task/<int:task_list_id>/', views.create_task, name='create_task'),
    path('update_task_list/<int:task_list_id>/', views.update_task_list, name='update_task_list'),
    path('delete_task_list/<int:task_list_id>/', views.delete_task_list, name='delete_task_list'),
    path('update_task/<int:task_id>/', views.update_task, name='update_task'),
    path('delete_task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('mark_done/<int:task_id>/', views.mark_done, name='mark_done'),
    path('search/', views.search_tasks, name='search_tasks'),
    path('export_task_lists/', views.export_task_lists, name='export_task_lists'),
    path('task_list/<int:task_list_id>/', views.task_list, name='task_list'),
    path('logout/', views.user_logout, name='user_logout'),
]