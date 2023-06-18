from django.db.models import QuerySet
from django.http import HttpResponse
from ..models import Task, User


def create_user(user_form) -> None:
    """Создание пользователя"""
    user = user_form.save(commit=False)
    user.set_password(user_form.cleaned_data['password'])
    user.save()

def create_task(form, user: User) -> None:
    """Создание задания"""
    task = form.save(commit=False)
    task.user = user
    task.save()

def completion_task(pk: int) -> None:
    """Изменение статуса задания на 'выполнено'"""
    task = Task.objects.get(pk=pk)
    task.status = 'выполнено'
    task.save()