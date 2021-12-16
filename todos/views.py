from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .models import *
from .permissions import IsOwner
from .serializers import *


@api_view(['GET'])
def api_root(request, format=None):
    """
    API root view which give the urls of the available endpoints.
    """
    return Response({
        'tasks': reverse('task-list', request=request, format=format),
        'todos': reverse('tasklist-list', request=request, format=format),
        'docs': reverse('swagger-ui', request=request, format=format)
    })

class TaskListView(generics.ListCreateAPIView):
    """
    API endpoint that allows tasks to be viewed & created. \n
    Only accessible to authenticated users who can only see their own tasks.
    """
    serializer_class = TaskSerializer

    def get_queryset(self):
        # Making sure the current user only see his own tasks
        queryset = Task.objects.filter(user=self.request.user)

        # Fetching optional query parameters
        query = self.request.GET.get('list')
        status = self.request.GET.get('done')

        # Returning the queryset filtered by the query parameters
        if query is not None:
            queryset = queryset.filter(task_list__name__contains=query)
        if status is not None:
            status = status.capitalize()
            queryset = queryset.filter(done=status)
        return queryset


    def perform_create(self, serializer):
        # Creating a new task for the current user
        t = serializer.save(user=self.request.user)

    permission_classes = [permissions.IsAuthenticated, IsOwner]


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that allows tasks to be edited or deleted
    Only accessible to the owner of the task
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    permission_classes = [permissions.IsAuthenticated, IsOwner]


class TaskListListView(generics.ListCreateAPIView):
    """
    API endpoint that allows tasklists to be viewed & created
    Only accessible to authenticated users who can only see their own tasks
    """    
    serializer_class = TaskListSerializer

    def get_queryset(self):
        # Making sure the current user only see his own tasklists
        return TaskList.objects.filter(user=self.request.user.id)

    def perform_create(self, serializer):
        # Creating a new tasklist for the current user
        serializer.save(user=self.request.user)

    permission_classes = [permissions.IsAuthenticated, IsOwner]


class TaskListDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that allows tasklists to be edited or deleted
    Only accessible to the owner of the task
    """
    queryset = TaskList.objects.all()
    serializer_class = TaskListSerializer

    permission_classes = [permissions.IsAuthenticated, IsOwner]
