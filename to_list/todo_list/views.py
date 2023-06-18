from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from .forms import RegisterUserForm, LoginUserForm, TaskForm
from .services import create_user, create_task, completion_task
from .models import Task


def index(request):
    return render(request, 'index.html')


def register(request):
    """Регистрация нового пользователя"""
    user_form = RegisterUserForm(request.POST or None)
    if request.method == "POST":
        if user_form.is_valid():
            create_user(user_form)
            return redirect(reverse_lazy('login'))
    return render(request, 'registr.html', {'user_form': user_form})


class LoginView(LoginView):
    """Вход пользователя"""
    form_class = LoginUserForm
    template_name = 'login.html'


class LogoutView(LogoutView):
    """Выход пользователя"""
    template_name = 'logout.html'


@login_required
def add_task(request):
    """Создание задания"""
    task_form = TaskForm(request.POST or None)
    print(request.user.telegram_acc)
    if request.method == "POST":
        if task_form.is_valid():
            create_task(task_form, request.user)
            return redirect(reverse_lazy('get_tasks'))
    return render(request, 'add.html', {'form': task_form})


@login_required
def delete_task(request, pk):
    """Удаление задания"""
    if request.method == "POST":
        task = Task.objects.get(pk=pk)
        task.delete()
        return redirect(reverse_lazy('get_tasks'))


@login_required
def complete_task(request, pk):
    """Выполнение задания"""
    if request.method == "POST":
        completion_task(pk)
        return redirect(reverse_lazy('get_tasks'))


@login_required
def get_tasks_user(request):
    """Получение списка заданий пользователя"""
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'get_tasks.html', {'tasks': tasks})
