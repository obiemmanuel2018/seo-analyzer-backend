from django.urls import path
from .views import analyzer


app_name = "spider"

urlpatterns = [
    path('', view=analyzer)
]
