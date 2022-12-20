import stripe
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from .models import Price, Product

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.


class HomeView(TemplateView):
    template_name = "payments/pages/home.html"

    def get_context_data(self, **kwargs):
        product = Product.objects.get(name="Couse Django")
        prices = Price.objects.filter(product=product)
        context = super(HomeView,
                        self).get_context_data(**kwargs)
        context.update({
            "product": product,
            "prices": prices
        })
        return context


class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        price = Price.objects.get(id=self.kwargs["pk"])
        domain = "https://yourdomain.com"
        if settings.DEBUG:
            domain = "http://127.0.0.1:8000"
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': price.stripe_price_id,
                    'quantity': 1,
                },
            ],
            metadata={
                'price_id': price.id,
            },
            mode='payment',
            success_url=domain + '/success/',
            cancel_url=domain + '/cancel/',
        )
        return redirect(checkout_session.url)


class SuccessView(TemplateView):
    template_name = "payments/pages/success.html"


class CancelView(TemplateView):
    template_name = "payments/pages/cancel.html"


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        customer_email = session["customer_details"]["email"]
        line_itens = stripe.checkout.Session.list_line_items(session["id"])
        stripe_price_id = line_itens["data"][0]["price"]["id"]
        price = Price.objects.get(stripe_price_id=stripe_price_id)
        product = price.product
        send_mail(
            subject="Here is your product",
            message=f"thanks for you purchase, here is your product: {product.url}",  # noqa
            recipient_list=[customer_email],
            from_email="heitorlouzeirodev@gmail.com",
            fail_silently=False,
        )

    return HttpResponse(status=200)


class CustomPaymentView(TemplateView):
    template_name = "payments/pages/custom_payment.html"

    def get_context_data(self, **kwargs):
        product = Product.objects.get(name="Couse Django")
        prices = Price.objects.filter(product=product)
        context = super(CustomPaymentView, self).get_context_data(**kwargs)
        context.update({
            "product": product,
            "prices": prices,
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
        })
        return context


class StripeIntentView(View):
    def post(self, request, *args, **kwargs):
        try:
            product_id = self.kwargs["pk"]
            product = Price.objects.get(id=product_id)
            intent = stripe.PaymentIntent.create(
                amount=product.price,
                currency='usd',
            )
            return JsonResponse({
                'clientSecret': intent['client_secret']
            })
        except Exception as e:
            return JsonResponse({'error': str(e)})
