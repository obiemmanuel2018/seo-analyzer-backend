from django.shortcuts import render
from .main import analyzer as main_analyzer
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import ProjectSerializer, ResultSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.contrib.auth import get_user_model
from .models import Project

# Create your views here.



# seo analyzer

@api_view(['GET'])
def analyzer(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        return Response("Project Doesn't Exist", status=status.HTTP_404_NOT_FOUND)
    results = main_analyzer(project.name, project.homepage)
    results['project'] = project
    result_serializer = ResultSerializer(data=results)
    if result_serializer.is_valid():
       result_serializer.save()
       return  Response(result_serializer.data,status=status.HTTP_200_OK )
    else:
        return  Response(result_serializer.errors,status=status.HTTP_400_BAD_REQUEST )





@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def projectsList(request):

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
            return Response(project_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

