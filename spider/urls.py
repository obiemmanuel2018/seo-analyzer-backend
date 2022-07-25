from django.urls import path, re_path
from .views import analyzer, ProjectDetail, projectList, articles


app_name = "spider"

urlpatterns = [
    re_path(r'^analyze-project/(?P<project_id>[0-9]+)/$', view=analyzer),
    re_path(r'^projects/(?P<id>[0-9]+)/$', view=ProjectDetail),
    re_path(r'^projects/$', view=projectList),
    re_path(r'^articles/$', view=articles)
]
