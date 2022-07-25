from rest_framework import permissions
from .models import Subscription
from django.conf import settings

class hasSubscribed(permissions.BasePermission):
    message = "You dont have any active subscription. Please subscribe to continue!"
    def has_permission(self, request, view):
        try:
           subscription = Subscription.objects.get(user=request.user)
           return subscription.is_valid()
        except Subscription.DoesNotExist:
            return False
        except:
            return False