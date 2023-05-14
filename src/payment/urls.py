from django.urls import path
from paypal.standard.ipn import views as paypal_views

from payment.views import Department, Order, Payment

urlpatterns = [
    path("paypal-ipn/", paypal_views.ipn, name="paypal-ipn"),
    path("order/", Order.as_view(), name="order"),
    path("department/", Department.as_view(), name="department"),
    path("payment/", Payment.as_view(), name="payment"),
]
