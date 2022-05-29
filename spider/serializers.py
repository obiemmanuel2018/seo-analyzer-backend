from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Project, Result



class ResultSerializer(serializers.ModelSerializer):
     project = serializers.SlugRelatedField(queryset=Project.objects.all(), slug_field='name')
     class Meta:
         model = Result
         fields = (
             'id',
             'project',
             'duplicate_titles',
             'duplicate_descriptions',
             'missing_descriptions',
             'missing_titles',
             'missing_h1',
             'duplicate_h1',
             'missing_canonicals',
             'missing_viewports',
             'low_titles',
             'low_meta',
             'created_at',
             'updated_at'

         )
class ProjectSerializer(serializers.ModelSerializer):
     user = serializers.SlugRelatedField(queryset=get_user_model().objects.all(), slug_field='email')
     results = ResultSerializer(required=False)
     class Meta:
         model = Project
         fields = ('id', 'user','name', 'homepage','results')




