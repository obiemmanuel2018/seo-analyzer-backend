from django.shortcuts import render
from .main import analyzer as main_analyzer
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
# Create your views here.



# seo analyzer

@api_view(['GET'])
def analyzer(request):
    project_name = "shopital"
    homepage = "http://obi123.pythonanywhere.com/en/"
    results = main_analyzer(project_name, homepage)
    return  Response(results,status=status.HTTP_200_OK )
