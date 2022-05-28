from django.contrib import admin
from .models import Project

# Register your models here.

@admin.register(Project)
class ProjectsAdmin(admin.ModelAdmin):
      list_display = ('user', 'name', 'homepage', 'created_at')
      ordering = ('-created_at',)
      



