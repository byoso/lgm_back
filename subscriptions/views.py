import stripe

from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response

secret_key = "sk_test_51NSzlnCyzfytDBEqeBUQmR9R76L4o7HUJ4LIm4G6VxplqIFnK9gOWapeaar95pIqITOLrWr96yAIVWL9dDypTi3500oKVAaDCH"
stripe.api_key = secret_key


class CreateCheckoutSession(APIView):
    def post(self, request):
        price_id = request.data.get("priceId")

        try:
            session = stripe.checkout.Session.create(
                customer='cus_OFZMIvPNMVVAsz',
                success_url='http://localhost:8080/?#/account',
                # success_url='https://example.com/success.html?session_id={CHECKOUT_SESSION_ID}',
                cancel_url='http://localhost:8080/?#/account',
                mode='subscription',
                line_items=[{
                    'price': price_id,
                    # For metered billing, do not pass quantity
                    'quantity': 1
                }],
            )
            print('session id: ', session.id)
            print('session : ', session)
        except Exception as e:
            print(e)
            return Response({"message": "Backend error in a stripe session creation"}, 400)

        return Response({"message": "Subscription parameters sent to build the checkout page"})

    def get(self, request):
        pass


class Webhook(APIView):

    def post(self, request):
        print("=== webhook POST===")
        print(request.data)
        return Response({"message": "webhook received"})

    def get(self, request):
        print("=== webhook GET ===")
        print(request.data)
        return Response({"message": "webhook received"})
