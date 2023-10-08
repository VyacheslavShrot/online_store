from django.urls import path
from paypal.standard.ipn import views as paypal_views

from payment.views import Department, Order, Payment, OrderWorldwide, DepartmentWorldwide, PaymentWorldwide

urlpatterns = [
    path("paypal-ipn/", paypal_views.ipn, name="paypal-ipn"),
    path("order/", Order.as_view(), name="order"),
    path("department/", Department.as_view(), name="department"),
    path("payment/", Payment.as_view(), name="payment"),
    path("order/worldwide/", OrderWorldwide.as_view(), name="order_worldwide"),
    path("department/worldwide/", DepartmentWorldwide.as_view(), name="department_worldwide"),
    path("payment/worldwide/", PaymentWorldwide.as_view(), name="payment_worldwide"),
]
