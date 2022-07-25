from multiprocessing.reduction import duplicate
from django.shortcuts import render
from .main import analyzer as main_analyzer
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import ProjectSerializer, ArticleSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.contrib.auth import get_user_model
from .models import DuplicateDescription, LowTitle, MissingCanonical, MissingDescription, \
    MissingH1, MissingTitle, MissingViewPort, Project, Result, DuplicateTitle, LowMeta, CrawlingStatistic, AuditStatistic, Article
import os
from django.conf import settings
from datetime import datetime
# Create your views here.



# seo analyzer

@api_view(['POST'])
def analyzer(request, project_id):

    try:
        project = Project.objects.get(id=project_id)
        crawl_again = int(request.data.get('crawl_again', 0))
        if crawl_again:
             # register new crawler entry
            crawler_statistics = CrawlingStatistic.objects.create(
                project=project
            )
        
            crawler_statistics.save()
            try:
                crawled_file_path = os.path.join(settings.PROJECT_ROOT,project.name,'crawled.txt')
                with open(crawled_file_path,'w'):
                    pass
            except:
                pass
           
        try:
            Result.objects.get(project=project)
        except Result.DoesNotExist:
            crawler_statistics = CrawlingStatistic.objects.create(
                project=project
            )


        # register new audit entry
        audit_statistics = AuditStatistic.objects.create(
            project=project
        )
       
        audit_statistics.save()

    except Project.DoesNotExist:
        return Response("Project Doesn't Exist", status=status.HTTP_404_NOT_FOUND)
   
    results = main_analyzer(project.name, project.homepage)
    try:
        result = Result.objects.get(project=project)
        result.delete()
    except Result.DoesNotExist:
        pass
    result = Result.objects.create(
        project = project
    )
    result.save()

    result.save_duplicate_titles(DuplicateTitle, results['duplicate_titles'])
    result.save_duplicate_h1(DuplicateTitle, results['duplicate_h1'])
    result.save_duplicate_descriptions(DuplicateDescription, results['duplicate_descriptions'])
    result.save_missing_h1(MissingH1, results['missing_h1'])
    result.save_missing_titles(MissingTitle, results['missing_titles'])
    result.save_missing_descriptions(MissingDescription, results['missing_descriptions'])
    result.save_missing_canonical(MissingCanonical, results['missing_canonicals'])
    result.save_missing_viewport(MissingViewPort, results['missing_viewports'])
    result.save_low_titles(LowTitle, results['low_titles'])
    result.save_low_meta(LowMeta, results['low_metas'])

    return Response(results, status = status.HTTP_200_OK)





@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def projectList(request):

    if request.method == 'GET':
        projects = Project.objects.filter(user=request.user)
        project_serializer = ProjectSerializer(projects, many=True)
        return Response(project_serializer.data, status = status.HTTP_200_OK)
        
    if request.method == 'POST':
        data = request.data.copy()
        data['user'] = request.user
        project_serializer = ProjectSerializer(data=data)
        if project_serializer.is_valid():
            project_serializer.save()
            return Response(project_serializer.data, status = status.HTTP_201_CREATED)
        else:
            print(project_serializer.errors)
            return Response(project_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
def ProjectDetail(request, id):

    try:
        project = Project.objects.get(id=id)
    except Project.DoesNotExist:
        return Response('Project doesn\'t exist', )
    if request.method == 'GET':
         project_serializer = ProjectSerializer(project)
         return Response(project_serializer.data, status = status.HTTP_200_OK)

    if request.method == 'PUT':
        name = request.data.get('name', NULL)
        homepage = request.data.get('homepage', NULL)
        data = request.data.copy()
        data['user'] = request.user

        if not name:
            request.data['name'] = project.name
        if not homepage:
            request.data['homepage'] = project.homepage
        project_serializer = ProjectSerializer(project,data=data)

        if project_serializer.is_valid():

            try:
                new_project_name = request.data['name']
                if new_project_name != project.name:
                    old_projects_path = os.path.join(settings.PROJECT_ROOT,project.name)
                    new_projects_path = os.path.join(settings.PROJECT_ROOT,new_project_name)
                    os.rename(old_projects_path,new_projects_path )

            except:
                pass
            project_serializer.save()
            return Response(project_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(project_serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



def statistictics(request):
    crawler_statistics = CrawlingStatistic.objects.filter(date__year=datetime.now().year)
    audit_statistics = AuditStatistic.objects.filter(date__year=datetime.now().year)


@api_view(['GET'])
def articles(request):

    if request.method == "GET":
        articles = Article.objects.all()
        article_serializer = ArticleSerializer(articles, many=True)
        return Response(article_serializer.data, status = status.HTTP_200_OK)

    else:
        return Response(status = status.HTTP_400_BAD_REQUEST)

