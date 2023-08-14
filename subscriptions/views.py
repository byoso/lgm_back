import json

import stripe

from django.http import (
    JsonResponse,
    )
from django.contrib import messages


from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from django_silly_stripe.conf import SILLY_STRIPE as dss_conf
from django_silly_stripe.helpers import user_creates_new_customer, dev_log
from django_silly_stripe.models import (
    Product,
    Price,
    Customer,
    Subscription,
    )
from django_silly_stripe.serializers import (
    PriceSerializer,
)

from _adminplus.helpers import subscriptions_are_open


@api_view(['POST'])
def checkout(request):
    dev_log("===checkout view")
    if not subscriptions_are_open():
        return JsonResponse({"message": "Subscriptions are closed"}, status=403)
    if not request.user.is_authenticated or not request.user.is_active:
        return JsonResponse({"message": "Permission denied"}, status=403)
    if request.method == 'POST':
        data = json.loads(request.body)
        # print("===data: ", data)
        price_id = data["priceId"]

        stripe.api_key = dss_conf["DSS_SECRET_KEY"]
        user = request.user
        if not hasattr(user, 'customer'):
            # print("===new_customer_data: ", new_customer_data)
            user_creates_new_customer(user)

        else:
            if dss_conf['SUBSCRIBE_ONLY_ONCE']:
                product = Price.objects.get(id=price_id).product
                if Subscription.objects.filter(
                        customer=user.customer,
                        product=product,
                        status='active',
                        ).exists():
                    return JsonResponse(
                        {"message": "You already have an active subscription"},
                        status=403,
                        )

        try:
            # print("===request.META['HTTP_HOST']: ", request.META['HTTP_HOST'])
            session = stripe.checkout.Session.create(
                customer=user.customer.id,
                success_url=dss_conf['SUCCESS_URL'],
                cancel_url=dss_conf['SUCCESS_URL'],
                mode='subscription',
                line_items=[{
                    'price': price_id,
                    # For metered billing, do not pass quantity
                    'quantity': 1
                }],
            )
            # print('session id: ', session.id)
            # print('session : ', session)
        except Exception as e:
            # print(e)
            return JsonResponse(
                {"message": "Backend error in a stripe session creation"},
                status=500,
                )

        return JsonResponse(
            {
                "message": "Subscription parameters sent to build the checkout page",
                "url": session.url,
            },
            status=200,
            )
