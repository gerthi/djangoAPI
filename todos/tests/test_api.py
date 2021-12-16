from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from todos.models import Task, TaskList


class TaskEndpointTests(APITestCase):
    """
    Testing the tasks endpoints
    """

    def setUp(self):
        """
        Creating two users and one task for the tests
        """
        self.user1 = User.objects.create_user(username='user2', password='test')
        self.user2 = User.objects.create_user(username='user1', password='test')
        self.client.force_authenticate(self.user1)
        data = {
            'name': 'Test Task',
            'done': False,
            'priority': 1,
        }
        self.client.post('/tasks/', data)

    def test_task_list(self):
        """
        An user can access his tasks
        """
        response = self.client.get('/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_task_creation(self):
        """
        An user can create a task
        """
        data = {
            'name': 'Test Task 2',
            'done': False,
            'priority': 1,
        }
        response = self.client.post('/tasks/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)

    def test_task_update(self):
        """
        An user can update his own tasks
        """
        task = Task.objects.get(name='Test Task')
        t_id = task.id
        response = self.client.patch('/tasks/{}/'.format(task.id), {'name': 'Updated Task', 'done': True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.get(pk=t_id).name, 'Updated Task')
        self.assertEqual(Task.objects.get(pk=t_id).done, True)

    def test_task_pemissions(self):
        """
        An user can only see his own tasks
        """
        self.client.force_authenticate(self.user2)
        
        response = self.client.get('/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

        response = self.client.get('/tasks/1/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_task_destroy(self):
        """
        An user can delete his own tasks (and only his own)
        """
        self.client.force_authenticate(self.user2)
        response = self.client.delete('/tasks/1/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(self.user1)
        response = self.client.delete('/tasks/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TaskListEndpointTests(APITestCase):
    """
    Testing the tasklist endpoints
    """

    @classmethod
    def setUpTestData(cls):
        """
        Creating two users and two tasks for the tests
        """
        cls.user1 = User.objects.create_user(username='user2', password='test')
        cls.user2 = User.objects.create_user(username='user1', password='test')
        cls.task1 = Task.objects.create(name='Test Task u1', done=False, priority=1, user=cls.user1)
        cls.task2 = Task.objects.create(name='Test Task u2', done=False, priority=1, user=cls.user2)
        cls.tasklist1 = TaskList.objects.create(name='Test Tasklist u1', user=cls.user1)
        cls.tasklist2 = TaskList.objects.create(name='Test Tasklist u2', user=cls.user2)

    def setUp(self):
        """
        Authenticating the user 1 for the tests
        """
        self.client.force_authenticate(self.user1)

    def test_tasklist_creation(self):
        """
        An user can create a new tasklist
        """
        response = self.client.post('/tasklist/', {'name': 'Tasklist User 1'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TaskList.objects.filter(user=self.user1).count(), 2)

    def test_tasklist_list(self):
        """
        An user can access his tasklists 
        """
        response = self.client.get('/tasklist/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_add_tasks_to_tasklist(self):
        """
        An user can add only add his own tasks to his tasklists
        """
        response = self.client.patch('/tasks/2/', {'task_list': self.tasklist1.id}) 
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        response = self.client.patch('/tasks/1/', {'task_list': self.tasklist1.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.tasklist1.tasks.count(), 1)
        
    def test_tasklist_update(self):
        """
        An user can update his own tasklists
        """
        response = self.client.patch('/tasklist/1/', {'name': 'Updated Tasklist'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(TaskList.objects.get(pk=self.tasklist1.id).name, 'Updated Tasklist')

    def test_tasklist_pemissions(self):
        """
        An user can only see his own tasklists
        """
        response = self.client.get('/tasklist/2/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_tasklist_destroy(self):
        """
        An user can delete his own tasklists (and only his own)
        """
        response = self.client.delete('/tasklist/2/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.delete('/tasklist/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
