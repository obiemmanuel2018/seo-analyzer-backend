from django.urls import re_path
from . import views


app_name = "payment"

urlpatterns = [
    re_path(r"^subscription-plans/$", views.subscription_plans),
    re_path(r"^subscribe", views.subscribe),
]
