from dataclasses import field, fields
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Article, CrawlingStatistic, DuplicateDescription, LowTitle, MissingCanonical, MissingDescription, \
    MissingH1, MissingTitle, MissingViewPort, Project, Result, DuplicateTitle, LowMeta, DuplicateH1, ArticleContent

class DuplicateTitleSerializer(serializers.ModelSerializer):
   
      class Meta:
          model = DuplicateTitle
          fields = ('titles',)

class DuplicateH1Serializer(serializers.ModelSerializer):
      
      class Meta:
          model = DuplicateH1
          fields = ('titles',)

class DuplicateDescriptionSerializer(serializers.ModelSerializer):
      
      class Meta:
          model = DuplicateDescription
          fields = ('titles',)

class MissingTitleSerializer(serializers.ModelSerializer):
      
      class Meta:
          model = MissingTitle
          fields = ('title',)

class MissingDescriptionSerializer(serializers.ModelSerializer):
      
      class Meta:
          model = MissingDescription
          fields = ('title', )
class MissingH1Serializer(serializers.ModelSerializer):
    
    class Meta:
        model = MissingH1
        fields = ('title', )

class MissingCanonicalSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MissingCanonical
        fields = ('title', )

class MissingViewPortSerializer(serializers.ModelSerializer):
      
      class Meta:
          model = MissingViewPort
          fields = ('title',)

class LowTitleSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = LowTitle
        fields = ('title',)

class LowMetaSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = LowMeta
        fields = ('title',)



class ResultSerializer(serializers.ModelSerializer):
     project = serializers.SlugRelatedField(queryset=Project.objects.all(), slug_field='name')
     duplicate_titles = DuplicateTitleSerializer(many=True)
     duplicate_h1 = DuplicateH1Serializer(many=True)
     duplicate_descriptions = DuplicateDescriptionSerializer(many=True)
     missing_descriptions = MissingDescriptionSerializer(many=True)
     missing_titles = MissingTitleSerializer(many=True)
     missing_h1 = MissingH1Serializer(many=True)
     missing_canonicals = MissingCanonicalSerializer(many=True)
     missing_viewports = MissingViewPortSerializer(many=True)
     low_titles = LowTitleSerializer(many=True)
     low_metas = LowMetaSerializer(many=True)

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
             'low_metas',
             'created_at',
             'updated_at'

         )



class ProjectSerializer(serializers.ModelSerializer):
     user = serializers.SlugRelatedField(queryset=get_user_model().objects.all(), slug_field='email')
     results = ResultSerializer(many=False, read_only=True)


    
     class Meta:
         model = Project
         fields = ('id', 'user','name', 'homepage','results','crawl_statistics', 'aud_statistics','crawled_links')


class ArticleContentSerializer(serializers.ModelSerializer):
      class Meta:
          model = ArticleContent
          fields = ('id','title','content')
class ArticleSerializer(serializers.ModelSerializer):
      contents = ArticleContentSerializer(many=True)
      class Meta:
          model = Article
          fields =('id','title', 'contents')



