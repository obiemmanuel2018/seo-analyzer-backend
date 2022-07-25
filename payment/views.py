from rest_framework import response
from rest_framework.response import Response
from .utils import add_months, substract_month
from django.conf import settings
import datetime
from rest_framework.decorators import api_view, permission_classes
from .models import Subscription
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
import datetime
from .utils import add_months


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def subscription_plans(request):
    data = [
        {
            "subscription_type": "free",
            "category": "free plan",
            "amount": "0 XFA",
            "description": "30 days free trial ( to get started for free)",
        },
        {
            "subscription_type": "month",
            "category": "baby plan",
            "amount": "5,000 XFA",
            "description": "30 days free trial + 1 month unlimited use 5,000XFA/month billed month-to-month",
        },
        {
            "subscription_type": "year",
            "category": "business plan",
            "amount": "54,000 XFA",
            "description": "30 days free trial + 12 month with 10% discount  60,000XFA -  54,000XFA save 6,000XFA Billed yearly",
        },
    ]
    return Response(data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes(
    [
        IsAuthenticated,
    ]
)
def subscribe(request):
    if request.method == "POST":
        data = request.data.copy()
        data["user"] = request.user

        if data["payment_method"] == "MTN":
            data["payment_method"] = "mtn money"
        else:
            data["payment_method"] = "orange money"
        try:
            subscription = Subscription.objects.get(user=request.user)
            if data["type"] == "month":
                data["valid_to"] = add_months(subscription.valid_to, 1)
            else:
                data["valid_to"] = add_months(subscription.valid_to, 12)
            subscription.valid_to = data["valid_to"]
            subscription.subscription_type = data["type"]
            subscription.payment_method = data["payment_method"]

        except Subscription.DoesNotExist:
            if data["type"] == "month":
                data["valid_to"] = add_months(datetime.date.today(), 1)
            else:
                data["valid_to"] = add_months(datetime.date.today(), 12)
            subscription = Subscription.objects.create(
                id=request.user.email,
                user=request.user,
                valid_to=data["valid_to"],
                subscription_type=data["type"],
                account_type="paid",
                payment_method=data["payment_method"],
            )

        subscription.save()
        return Response(
            {
                "id": subscription.id,
                "user": subscription.user.email,
                "valid_to": subscription.valid_to,
                "payment_method": subscription.payment_method,
                "subscription_type": subscription.subscription_type,
            },
            status=status.HTTP_200_OK,
        )

    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
