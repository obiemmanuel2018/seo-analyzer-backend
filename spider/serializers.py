from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
     user = serializers.SlugRelatedField(queryset=get_user_model().objects.all(), slug_name = 'user')
     class Meta:
         model = Project
         fields = ('id', 'user','name', 'homepage')
