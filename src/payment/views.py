from django.contrib import messages
from django.dispatch import receiver
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView, TemplateView
from paypal.standard.forms import PayPalPaymentsForm
from paypal.standard.ipn.signals import valid_ipn_received

from payment.forms import DepartmentForm, OrderForm
from payment.services.emails import send_registration_email
from store.models import Product
from store.views import get_cart_items


class Order(TemplateView, FormView):
    http_method_names = ["get", "post"]
    form_class = OrderForm
    template_name = "order.html"
    success_url = "/department/"

    def get(self, request, *args, **kwargs):
        cart_items, total = get_cart_items(request)
        form_data = request.session.get("order_data")
        if form_data:
            form = self.form_class(initial=form_data)
        else:
            form = self.form_class()
        return render(request, "order.html", {"total": total, "cart_items": cart_items, "form": form})

    def form_valid(self, form):
        name = form.cleaned_data["name"]
        surname = form.cleaned_data["surname"]
        email = form.cleaned_data["email"]
        phone_number = form.cleaned_data["phone_number"]
        city = form.cleaned_data["city"]

        self.request.session["order_data"] = {
            "name": name,
            "surname": surname,
            "email": email,
            "phone_number": str(phone_number),
            "city": city,
        }

        return redirect(self.success_url)

    def form_invalid(self, form):
        cart_items, total = get_cart_items(self.request)
        return self.render_to_response(self.get_context_data(form=form, cart_items=cart_items, total=total))


class Department(TemplateView, FormView):
    http_method_names = ["get", "post"]
    form_class = DepartmentForm
    template_name = "department.html"
    success_url = "/payment/"

    def get(self, request, *args, **kwargs):
        cart_items, total = get_cart_items(request)
        order_data = request.session.get("order_data")
        city = order_data.get("city")
        form = self.form_class(city=city)

        return render(request, "department.html", {"total": total, "cart_items": cart_items, "form": form})

    def form_valid(self, form):
        department = form.cleaned_data["department"]
        description = form.cleaned_data["description"]
        self.request.session["order_department"] = {"department": department, "description": description}
        return redirect(self.success_url)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "An error occurred while submitting the form or there is no post office in your city. Please "
            "try again.",
        )
        return redirect("/order/")


class Payment(TemplateView, FormView):
    http_method_names = ["get", "post"]

    @csrf_exempt
    def get(self, request, *args, **kwargs):
        order_data = request.session.get("order_data")
        order_department = request.session.get("order_department")
        cart_items, total = get_cart_items(request)

        item_name = "Order from sle3pinghood"
        paypal_dict = {
            "business": "slavikshrot@gmail.com",
            "amount": total,
            "currency_code": "USD",
            "item_name": item_name,
            "invoice": str(item_name),
            "notify_url": request.build_absolute_uri(reverse("paypal-ipn")),
            "return_url": request.build_absolute_uri(reverse("store:cart")),
            "cancel_return": request.build_absolute_uri(reverse("payment")) + "?cancel=1&custom={}".format(item_name),
        }
        payment_form = PayPalPaymentsForm(initial=paypal_dict)

        if order_data:
            name = order_data.get("name")
            surname = order_data.get("surname")
            email = order_data.get("email")
            phone_number = order_data.get("phone_number")
            city = order_data.get("city")
            department = order_department.get("department")
            description = order_department.get("description")
            send_registration_email(
                total,
                cart_items,
                name=name,
                surname=surname,
                email=email,
                phone_number=phone_number,
                city=city,
                department=department,
                description=description,
            )

        return render(
            request, "payment.html", {"total": total, "payment_form": payment_form, "cart_items": cart_items}
        )

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        ipn_obj = request.POST
        if ipn_obj.get("txn_type") == "web_accept" and ipn_obj.get("payment_status") == "Completed":
            # Done payment
            cart_items, total = get_cart_items(ipn_obj.get("invoice"))
            # item_name = "Order from sle3pinghood"
            send_registration_email(str(total), str(cart_items))

        return HttpResponse(status=200)


@receiver(valid_ipn_received)
def payment_notification(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.get("txn_type") == "web_accept" and ipn_obj.get("payment_status") == "Completed":
        # Done payment
        cart_items, total = get_cart_items(ipn_obj.get("invoice"))
        # item_name = "Order from sle3pinghood"
        send_registration_email(str(total), str(cart_items))
