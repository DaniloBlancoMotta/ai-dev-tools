from django.contrib import admin
from .models import Todo

# Register your models here.

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('title', 'due_date', 'resolved', 'created_at')
    list_filter = ('resolved', 'due_date', 'created_at')
    search_fields = ('title', 'description')
    list_editable = ('resolved',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
