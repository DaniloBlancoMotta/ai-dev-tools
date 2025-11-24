from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import date, timedelta
from .models import Todo


class TodoModelTest(TestCase):
    """Tests for the Todo model"""
    
    def setUp(self):
        self.todo = Todo.objects.create(
            title="Test TODO",
            description="Test description",
            due_date=date.today() + timedelta(days=7)
        )
    
    def test_todo_creation(self):
        """Test that a TODO can be created"""
        self.assertEqual(self.todo.title, "Test TODO")
        self.assertEqual(self.todo.description, "Test description")
        self.assertFalse(self.todo.resolved)
        
    def test_todo_str_representation(self):
        """Test the string representation of a TODO"""
        self.assertEqual(str(self.todo), "Test TODO")
    
    def test_todo_default_resolved_status(self):
        """Test that TODOs are not resolved by default"""
        todo = Todo.objects.create(title="Another TODO")
        self.assertFalse(todo.resolved)
    
    def test_todo_optional_fields(self):
        """Test that description and due_date are optional"""
        todo = Todo.objects.create(title="Minimal TODO")
        self.assertEqual(todo.description, "")
        self.assertIsNone(todo.due_date)
    
    def test_todo_ordering(self):
        """Test that TODOs are ordered by created_at descending"""
        todo1 = Todo.objects.create(title="First")
        todo2 = Todo.objects.create(title="Second")
        todos = Todo.objects.all()
        self.assertEqual(todos[0], todo2)
        self.assertEqual(todos[1], todo1)


class TodoViewsTest(TestCase):
    """Tests for the Todo views"""
    
    def setUp(self):
        self.client = Client()
        self.todo = Todo.objects.create(
            title="Test TODO",
            description="Test description",
            due_date=date.today()
        )
    
    def test_todo_list_view(self):
        """Test the TODO list view"""
        response = self.client.get(reverse('todo_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todos/todo_list.html')
        self.assertContains(response, "Test TODO")
    
    def test_todo_list_empty(self):
        """Test TODO list when no TODOs exist"""
        Todo.objects.all().delete()
        response = self.client.get(reverse('todo_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No TODOs yet!")
    
    def test_todo_create_view_get(self):
        """Test GET request to create TODO view"""
        response = self.client.get(reverse('todo_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todos/todo_form.html')
    
    def test_todo_create_view_post(self):
        """Test POST request to create a new TODO"""
        data = {
            'title': 'New TODO',
            'description': 'New description',
            'due_date': '2025-12-31'
        }
        response = self.client.post(reverse('todo_create'), data)
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertTrue(Todo.objects.filter(title='New TODO').exists())
    
    def test_todo_create_without_optional_fields(self):
        """Test creating a TODO without optional fields"""
        data = {'title': 'Minimal TODO'}
        response = self.client.post(reverse('todo_create'), data)
        self.assertEqual(response.status_code, 302)
        todo = Todo.objects.get(title='Minimal TODO')
        self.assertEqual(todo.description, '')
        self.assertIsNone(todo.due_date)
    
    def test_todo_edit_view_get(self):
        """Test GET request to edit TODO view"""
        response = self.client.get(reverse('todo_edit', args=[self.todo.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todos/todo_form.html')
        self.assertContains(response, "Test TODO")
    
    def test_todo_edit_view_post(self):
        """Test POST request to edit a TODO"""
        data = {
            'title': 'Updated TODO',
            'description': 'Updated description',
            'due_date': '2025-12-25'
        }
        response = self.client.post(reverse('todo_edit', args=[self.todo.pk]), data)
        self.assertEqual(response.status_code, 302)
        self.todo.refresh_from_db()
        self.assertEqual(self.todo.title, 'Updated TODO')
        self.assertEqual(self.todo.description, 'Updated description')
    
    def test_todo_delete_view_get(self):
        """Test GET request to delete TODO view"""
        response = self.client.get(reverse('todo_delete', args=[self.todo.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todos/todo_confirm_delete.html')
        self.assertContains(response, "Test TODO")
    
    def test_todo_delete_view_post(self):
        """Test POST request to delete a TODO"""
        todo_pk = self.todo.pk
        response = self.client.post(reverse('todo_delete', args=[todo_pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Todo.objects.filter(pk=todo_pk).exists())
    
    def test_todo_toggle_resolved(self):
        """Test toggling the resolved status of a TODO"""
        self.assertFalse(self.todo.resolved)
        
        response = self.client.get(reverse('todo_toggle_resolved', args=[self.todo.pk]))
        self.assertEqual(response.status_code, 302)
        self.todo.refresh_from_db()
        self.assertTrue(self.todo.resolved)
        
        response = self.client.get(reverse('todo_toggle_resolved', args=[self.todo.pk]))
        self.todo.refresh_from_db()
        self.assertFalse(self.todo.resolved)
    
    def test_todo_edit_nonexistent(self):
        """Test editing a non-existent TODO returns 404"""
        response = self.client.get(reverse('todo_edit', args=[9999]))
        self.assertEqual(response.status_code, 404)
    
    def test_todo_delete_nonexistent(self):
        """Test deleting a non-existent TODO returns 404"""
        response = self.client.get(reverse('todo_delete', args=[9999]))
        self.assertEqual(response.status_code, 404)


class TodoIntegrationTest(TestCase):
    """Integration tests for complete TODO workflows"""
    
    def setUp(self):
        self.client = Client()
    
    def test_complete_todo_lifecycle(self):
        """Test creating, editing, toggling, and deleting a TODO"""
        # Create
        response = self.client.post(reverse('todo_create'), {
            'title': 'Integration Test TODO',
            'description': 'Testing full lifecycle',
            'due_date': '2025-12-31'
        })
        self.assertEqual(response.status_code, 302)
        todo = Todo.objects.get(title='Integration Test TODO')
        
        # Edit
        response = self.client.post(reverse('todo_edit', args=[todo.pk]), {
            'title': 'Updated Integration Test',
            'description': 'Updated description',
            'due_date': '2025-12-25'
        })
        todo.refresh_from_db()
        self.assertEqual(todo.title, 'Updated Integration Test')
        
        # Toggle resolved
        response = self.client.get(reverse('todo_toggle_resolved', args=[todo.pk]))
        todo.refresh_from_db()
        self.assertTrue(todo.resolved)
        
        # Delete
        response = self.client.post(reverse('todo_delete', args=[todo.pk]))
        self.assertFalse(Todo.objects.filter(pk=todo.pk).exists())
