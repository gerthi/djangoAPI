from django.db import models

class Task(models.Model):
    name = models.CharField(max_length=255)
    done = models.BooleanField(default=False)
    priority = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    task_list =models.ForeignKey('TaskList', related_name='tasks', on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
        
    class Meta:
        ordering = ['priority', '-created_at']

class TaskList(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.name