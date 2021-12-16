from rest_framework import serializers
from .models import *


class TaskListsForeignKey(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        return TaskList.objects.filter(user=self.context['request'].user)


class TaskSerializer(serializers.ModelSerializer):
    task_list = TaskListsForeignKey(required=False)

    class Meta:
        model = Task
        fields = ('id', 'name', 'done', 'priority', 'task_list', 'created_at')
        read_only_fields = ('user',)


class TaskListSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = TaskList
        fields = ('id', 'name', 'tasks', 'created_at')


