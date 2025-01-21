from django.contrib import admin
from .models import Project, Task

# Register your models here.


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at')
    search_fields = ('name', 'description', 'owner__username')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'assigned_to',
                    'status', 'due_date', 'created_at')
    list_filter = ('status', 'assigned_to', 'project')
    search_fields = ('title', 'description')
