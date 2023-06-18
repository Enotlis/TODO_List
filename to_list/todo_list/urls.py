from django.urls import path
from todo_list import views

urlpatterns = [
    path('accounts/login/', views.LoginView.as_view(), name='login'),
    path('accounts/logout/', views.LogoutView.as_view(), name='logout'),
    path('accounts/register/', views.register, name='register'),
    path('tasks/get/', views.get_tasks_user, name='get_tasks'),
    path('task/add/', views.add_task, name='add_task'),
    path('task/delete/<int:pk>/', views.delete_task, name='delete_task'),
    path('tasks/complete/<int:pk>/', views.complete_task, name='complete_task'),
    path('', views.index, name='index')
]
