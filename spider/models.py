from django.db import models
from core.models import User
from django.contrib.postgres.fields import ArrayField
from datetime import datetime
import os
from django.conf import settings

# Create your models here.

class Project(models.Model):
      user = models.ForeignKey(User, related_name='projects', on_delete=models.CASCADE)
      name = models.CharField(max_length=100, unique=True)
      homepage = models.CharField(max_length=200, unique=True)
      crawling = models.BooleanField(default=False)
      auditing = models.BooleanField(default=False)
      created_at = models.DateTimeField(auto_now_add=True)
      updated_at = models.DateTimeField(auto_now=True)
      @property
      def crawl_statistics(self):
          data = {}
          statistics = self.crawling_statistics.filter(date__year=datetime.now().year)
    
          for stat in statistics:
            key = stat.date.strftime("%B")
            data[key] = data.get(key, 0) + 1
            
          return  {
                'labels' : list(data.keys()),
                'datasets' : {
                     'label':'Crawl Data',
                     'data':  list(data.values())
                }
            }
          
      @property
      def aud_statistics(self):
          data = {}
          statistics = self.audit_statistics.filter(date__year=datetime.now().year)
    
          for stat in statistics:
            key = stat.date.strftime("%B")
            data[key] = data.get(key, 0) + 1
            
          return  {
                'labels' : list(data.keys()),
                'datasets' : {
                    'label':'Crawl Data',
                     'data':  list(data.values())
                }
               
            }
      @property
      def crawled_links(self):
          crawled_file_path = os.path.join(settings.PROJECT_ROOT,self.name,'crawled.txt')
          links = []
          try:
            with open(crawled_file_path, 'r') as file:
                links = file.readlines()
          except:
            pass

          return links



      class Meta:
          ordering = ('-created_at',)

      def __str__(self):  
          return self.name

class Result(models.Model):
    project  = models.OneToOneField(Project, related_name="results", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.project.name

    def save_duplicate_titles(self,model, data):
        for titles in data:
            instance = model.objects.create(
                result = self,
                titles = titles
            )
            instance.save()

    def save_duplicate_h1(self,model, data):
        for titles in data:
            instance = model.objects.create(
                result = self,
                titles = titles
            )
            instance.save()

    def save_duplicate_descriptions(self, model, data):
        for titles in data:
            instance = model.objects.create(
                result = self,
                titles = titles
            )
            instance.save()

    def save_missing_h1(self, model, data):
        for title in data:
            instance = model.objects.create(
                result = self,
                title = title
            )
            instance.save()

    def save_missing_titles(self, model, data):
        for title in data:
            instance = model.objects.create(
                result = self,
                title = title
            )
            instance.save()

    def save_missing_descriptions(self, model, data):
        for title in data:
            instance = model.objects.create(
                result = self,
                title = title
            )
            instance.save()

    def save_missing_canonical(self, model, data):
        for title in data:
            instance = model.objects.create(
                result = self,
                title = title
            )
            instance.save()
            
    def save_missing_viewport(self, model, data):
        for title in data:
            instance = model.objects.create(
                result = self,
                title = title
            )
            instance.save()

    def save_low_titles(self, model, data):
        for title in data:
            instance = model.objects.create(
                result = self,
                title = title
            )
            instance.save()

    def save_low_meta(self, model, data):
        for title in data:
            instance = model.objects.create(
                result = self,
                title = title
            )
            instance.save()
        





class DuplicateTitle(models.Model):
      result = models.ForeignKey(Result, related_name="duplicate_titles", on_delete=models.CASCADE)
      titles = ArrayField(base_field = models.URLField(), blank=True)

      def __str__(self):
          return str(self.titles[0])

class DuplicateH1(models.Model):
      result = models.ForeignKey(Result, related_name="duplicate_h1", on_delete=models.CASCADE)
      titles = ArrayField(base_field = models.URLField(), blank=True)

      def __str__(self):
          return str(self.titles[0])

class DuplicateDescription(models.Model):
      result = models.ForeignKey(Result, related_name="duplicate_descriptions", on_delete=models.CASCADE)
      titles = ArrayField(base_field = models.URLField(), blank=True)


      def __str__(self):
          return str(self.titles[0])


class Title(models.Model):
      title = models.URLField()
      def __str__(self):
          return self.title


class MissingDescription(Title):
       result = models.ForeignKey(Result, related_name="missing_descriptions", on_delete=models.CASCADE)
     

class MissingTitle(Title):
       result = models.ForeignKey(Result, related_name="missing_titles", on_delete=models.CASCADE)
      
      
class MissingH1(Title):
       result = models.ForeignKey(Result, related_name="missing_h1", on_delete=models.CASCADE)

class MissingCanonical(Title):
       result = models.ForeignKey(Result, related_name="missing_canonicals", on_delete=models.CASCADE)
      

class MissingViewPort(Title):
       result = models.ForeignKey(Result, related_name="missing_viewports", on_delete=models.CASCADE)


class LowTitle(Title):
       result = models.ForeignKey(Result, related_name="low_titles", on_delete=models.CASCADE)
      

class LowMeta(Title):
      result = models.ForeignKey(Result, related_name="low_metas", on_delete=models.CASCADE)
      

    

class CrawlingStatistic(models.Model):
      project = models.ForeignKey(Project, related_name='crawling_statistics', on_delete=models.CASCADE)
      date = models.DateField(auto_now=datetime.date)
      

      def __str__(self):
          return str(self.date.year)


class AuditStatistic(models.Model):
      project = models.ForeignKey(Project, related_name='audit_statistics', on_delete=models.CASCADE)
      date = models.DateField(auto_now=datetime.now)


      def __str__(self):
         return str(self.date.year)


class Article(models.Model):
      title = models.CharField(max_length=255)

      def __str__(self):
          return self.title


class ArticleContent(models.Model):
      article = models.ForeignKey(Article, related_name='contents', on_delete=models.CASCADE)
      title = models.CharField(max_length=255,null=True)
      content = models.TextField()

      def __Str__(self):
          return self.title

      