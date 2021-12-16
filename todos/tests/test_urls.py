from django.contrib.auth.models import User
from django.test import SimpleTestCase
from django.urls import resolve, reverse
from rest_framework import status
from rest_framework.test import APITestCase
from todos.views import (TaskDetailView, TaskListDetailView, TaskListListView,
                         TaskListView)


class TestUrls(SimpleTestCase):
    """
    Testing that the endpoints urls are resolved correctly and views are called
    """
    
    def test_task_url_is_resolved(self):
        url = reverse('task-list')
        self.assertEquals(resolve(url).func.view_class, TaskListView)

    def test_task_detail_url_is_resolved(self):
        url = '/tasks/2/'
        self.assertEquals(resolve(url).func.view_class, TaskDetailView)

    def test_tasklist_url_is_resolved(self):
        url = reverse('tasklist-list')
        self.assertEquals(resolve(url).func.view_class, TaskListListView)

    def test_tasklist_detail_url_is_resolved(self):
        url = '/tasklist/34/'
        self.assertEquals(resolve(url).func.view_class, TaskListDetailView)


class UnauthenticatedTests(APITestCase):
    """
    An user can only access the API's endpoints if he is authenticated
    """

    def test_tasks_endpoint_unauthenticated(self):
        response = self.client.get('/tasks/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_taskdetail_endpoint_unauthenticated(self):
        response = self.client.get('/tasks/2/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_tasklists_endpoint_unauthenticated(self):
        response = self.client.get('/tasklist/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_tasklist_detail_endpoint_unauthenticated(self):
        response = self.client.get('/tasklist/3/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AuthenticatedTests(APITestCase):
    """
    An authenticated user can access the API's list endpoints
    """

    def setUp(self):
        """
        Creating & authenticating an user for the tests
        """
        user = User.objects.create_user(username='test', password='test')
        self.client.login(username='test', password='test')

    def test_tasks_endpoint_authenticated(self):
        """
        An authenticated user can access the task endpoint
        """
        response = self.client.get('/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_tasksdetail_endpoint_authenticated(self):
        """
        An authenticated user can access the task detail endpoint
        """
        response = self.client.get('/tasks/1/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_tasklists_endpoint_authenticated(self):
        """
        An authenticated user can access the tasklist endpoint
        """
        response = self.client.get('/tasklist/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_taskslist_detail_endpoint_authenticated(self):
        """
        An authenticated user can access the tasklist detail endpoint
        """
        response = self.client.get('/tasklist/1/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


