from django.urls import path

from payments.views import (CancelView, CreateCheckoutSessionView, HomeView,
                            SuccessView)

app_name = 'payments'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('success/', SuccessView.as_view(), name='success'),
    path('create-checkout-session/<pk>/',
         CreateCheckoutSessionView.as_view(), name='create-checkout-session')
]
