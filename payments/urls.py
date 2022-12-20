from django.urls import path

from payments.views import (CancelView, CreateCheckoutSessionView,
                            CustomPaymentView, HomeView, StripeIntentView,
                            SuccessView, stripe_webhook)

app_name = 'payments'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('webhooks/stripe/', stripe_webhook, name='stripe-webhook'),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('success/', SuccessView.as_view(), name='success'),
    path('create-checkout-session/<pk>/',
         CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('create-payment-intent/<pk>/',
         StripeIntentView.as_view(), name='create-payment-intent'),
    path('custom-payment/', CustomPaymentView.as_view(), name='custom-payment')

]
