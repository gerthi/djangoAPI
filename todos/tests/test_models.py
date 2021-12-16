from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.test import TestCase
from todos.models import Task, TaskList


class TaskModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
        Creating one user for the tests
        """
        cls.user1 = User.objects.create_user(username='user1', password='test')

    def test_task_creation_no_user(self):
        """
        A task can't be created without a user
        """
        with self.assertRaises(IntegrityError):
            Task.objects.create(name='Test Task')

    def test_task_creation(self):
        """
        A user can create a new task
        """
        task = Task.objects.create(name='Test Task', user=self.user1)
        self.assertIsNotNone(task.pk)
        self.assertEqual(task.name, 'Test Task')
        self.assertEqual(task.user, self.user1)
        self.assertEqual(task.priority, 1)
        self.assertFalse(task.done)

    def test_task_str(self):
        """
        The string representation of a task is its name
        """
        task = Task.objects.create(name='Test Task', user=self.user1)
        self.assertEqual(str(task), 'Test Task')

    def test_task_done(self):
        """
        A task is done when its done field is set to True
        """
        task = Task.objects.create(name='Test Task', user=self.user1, done=True)
        self.assertTrue(task.done)


class TaskListModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
        Creating one user and one taks for the tests
        """
        cls.user1 = User.objects.create(username='user1', password='test')
        cls.task1 = Task.objects.create(name='Test Task', user=cls.user1)

    def test_tasklist_creation_no_user(self):
        """
        A tasklist can't be created without a user
        """
        with self.assertRaises(IntegrityError):
            TaskList.objects.create(name='Test Tasklist')

    def test_tasklist_creation(self):
        """
        An user can create a new tasklist
        """
        tasklist = TaskList.objects.create(name='Test Tasklist', user=self.user1)
        tasklist.save()
        self.assertIsNotNone(tasklist.pk)
        self.assertEqual(tasklist.name, 'Test Tasklist')
        self.assertEqual(tasklist.user, self.user1)

    def test_tasklist_str(self):
        """
        The string representation of a tasklist is its name
        """
        tasklist = TaskList.objects.create(name='Test Task', user=self.user1)
        tasklist.save()
        self.assertEqual(str(tasklist), 'Test Task')

    def test_add_task_to_tasklist(self):
        """
        A task can be added to a tasklist
        """
        tasklist = TaskList.objects.create(name='Test Tasklist', user=self.user1)
        self.task1.task_list = tasklist
        self.task1.save()
        self.assertEqual(tasklist.tasks.count(), 1)
        self.assertEqual(self.task1.task_list, tasklist)

    def test_query_related_tasks(self):
        """
        Tasks can be queried by its tasklist
        """
        tasklist = TaskList.objects.create(name='Test Tasklist', user=self.user1)
        self.task1.task_list = tasklist
        self.task1.save()

        qs = Task.objects.filter(task_list__name__iexact='Test Tasklist')
        self.assertEqual(qs.count(), 1)
