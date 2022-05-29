from multiprocessing.reduction import duplicate
from typing import List
from django.db import models
from core.models import User
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField
# Create your models here.

class Project(models.Model):
      user = models.ForeignKey(User, related_name='projects', on_delete=models.CASCADE)
      name = models.CharField(max_length=100, unique=True)
      homepage = models.CharField(max_length=200, unique=True)
      created_at = models.DateTimeField(auto_now_add=True)
      updated_at = models.DateTimeField(auto_now=True)

      class Meta:
          ordering = ('-created_at',)

      def __str__(self):  
          return self.name


    
class Result(models.Model):
    project  = models.OneToOneField(Project, related_name="results", on_delete=models.CASCADE)
    duplicate_titles = ArrayField(base_field = models.TextField(), blank=True)
    duplicate_descriptions = ArrayField(base_field = models.TextField(), blank=True)
    missing_descriptions = ArrayField(base_field = models.TextField(), blank=True)
    missing_titles = ArrayField(base_field = models.TextField(), blank=True)
    missing_h1 = ArrayField(base_field = models.TextField(), blank=True)
    duplicate_h1 = ArrayField(base_field = models.TextField(), blank=True)
    missing_canonicals = ArrayField(base_field = models.TextField(), blank=True)
    missing_viewports = ArrayField(base_field = models.TextField(), blank=True)
    low_titles = ArrayField(base_field = models.TextField(), blank=True)
    low_meta = ArrayField(base_field = models.TextField(), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.project.name



