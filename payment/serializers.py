from .models import Subscription
from django.contrib.auth import get_user_model
from rest_framework import serializers



class SubscriptionSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(queryset = get_user_model(), slug_field='email')
    class Meta:
        model = Subscription
        fields = ('user', 'account_type', 'subscription_type','payment_method', 'valid_to')