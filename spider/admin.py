from django.contrib import admin
from .models import Project, Result

# Register your models here.

class ResultsAdmin(admin.TabularInline):
      model = Result
      fieldsets = (
        (None, {
            'fields': ('duplicate_titles', 'duplicate_descriptions','missing_descriptions' , 'missing_titles','missing_h1', 'duplicate_h1','missing_canonicals','missing_viewports','low_titles','low_meta' ,'created_at','updated_at')
        }),
       )
      readonly_fields = ('duplicate_titles', 'duplicate_descriptions','missing_descriptions' , 'missing_titles','missing_h1', 'duplicate_h1','missing_canonicals','missing_viewports','low_titles','low_meta' ,'created_at','updated_at')
      


@admin.register(Project)
class ProjectsAdmin(admin.ModelAdmin):
      list_display = ('user', 'name', 'homepage', 'created_at')
      ordering = ('-created_at',)
      inlines = [ResultsAdmin,]
      






