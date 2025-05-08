from django.urls import path
from .views import Payment
from .views import CreatePayment,GetMyPayments, GetMyLastPayment
urlpatterns = [
    path('api/payment/create',CreatePayment.as_view(),name='create-payment'),
    path('api/payment/get-my-all-payments',GetMyPayments.as_view(),name='get-my-payments'),
    path('api/payment/get-my-last-payments',GetMyLastPayment.as_view(),name='get-my-last-payments')
]