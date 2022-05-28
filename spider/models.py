from django.db import models
from core.models import User

# Create your models here.

class Project(models.Model):
      user = models.ForeignKey(User, related_name='projects', on_delete=models.CASCADE)
      name = models.CharField(max_length=100)
      homepage = models.CharField(max_length=200)
      created_at = models.DateTimeField(auto_now_add=True)
      updated_at = models.DateTimeField(auto_now_add=True)

      class Meta:
          ordering = ('-created_at',)

      def __str__(self):  
          return self.name