from .serializers import TaskSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from todo_list.models import Task, User

class WorkTask(APIView):
    """Получение списка задачь, создание задания"""
    def get(self, request):
        username=request.data['username']
        tasks = Task.objects.filter(user__telegram_acc=username)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        user = get_object_or_404(User, telegram_acc=request.data['username'])
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
