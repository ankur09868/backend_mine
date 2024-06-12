from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Tasks
from .serializers import TasksSerializer

class TaskListCreateAPIView(generics.ListCreateAPIView):
    queryset = Tasks.objects.all()
    serializer_class = TasksSerializer
    permission_classes = (AllowAny,)


class TaskRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tasks.objects.all()
    serializer_class = TasksSerializer
    permission_classes = (AllowAny,)

class UserTasksListAPIView(generics.ListAPIView):
    serializer_class = TasksSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Tasks.objects.filter(assigned_to_id=user_id)