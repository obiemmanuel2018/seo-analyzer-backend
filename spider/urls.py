from django.urls import path, re_path
from .views import *


app_name = "spider"

urlpatterns = [
    re_path(r'^analyze-project/(?P<project_id>[0-9]+)$', view=analyzer),
    re_path(r'^projects/', view=projectsList)
]
