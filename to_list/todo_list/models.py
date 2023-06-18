from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """Модель пользователя"""
    telegram_acc = models.CharField(max_length=45, blank=True,
                                    verbose_name='Телеграм аккаунт',
                                    help_text=('Введите telegram username, '
                                               'например @user.\n Для того чтобы пользоваться ботом'))
 

class Task(models.Model):
    """Модель задания"""
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    status = models.CharField(max_length=50, verbose_name='Статус',
                              default='не выполнено')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='Пользователь')