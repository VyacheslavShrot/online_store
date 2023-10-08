import os

from django.contrib import messages
from django.dispatch import receiver
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView, TemplateView
from paypal.standard.forms import PayPalPaymentsForm
from paypal.standard.ipn.signals import valid_ipn_received

from payment.forms import DepartmentForm, OrderForm, OrderWorldwideForm, DepartmentWorldwideForm
from payment.services.emails import send_order_email, send_order_client_email
# from payment.tasks import send_order_email_task
from store.models import Category
from store.views import sync_get_cart_items


class Order(TemplateView, FormView):
    http_method_names = ["get", "post"]
    form_class = OrderForm
    template_name = "order.html"
    success_url = "/department/"

    def get(self, request, *args, **kwargs):
        cart_items, total = sync_get_cart_items(request)
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
        self.request.session["current_step"] = "department"

        return redirect(self.success_url)

    def form_invalid(self, form):
        cart_items, total = sync_get_cart_items(self.request)
        return self.render_to_response(self.get_context_data(form=form, cart_items=cart_items, total=total))


class Department(TemplateView, FormView):
    http_method_names = ["get", "post"]
    form_class = DepartmentForm
    template_name = "department.html"
    success_url = "/payment/"

    def get(self, request, *args, **kwargs):
        current_step = request.session.get("current_step")
        if current_step != "department":
            return redirect(reverse("order"))

        cart_items, total = sync_get_cart_items(request)
        order_data = request.session.get("order_data")
        city = order_data.get("city")
        form = self.form_class(city=city)

        return render(request, "department.html", {"total": total, "cart_items": cart_items, "form": form})

    def form_valid(self, form):
        current_step = self.request.session.get("current_step")
        if current_step != "department":
            return HttpResponse(status=403)

        department = form.cleaned_data["department"]
        description = form.cleaned_data["description"]
        self.request.session["order_department"] = {"department": department, "description": description}

        self.request.session["current_step"] = "payment"

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
        current_step = request.session.get("current_step")
        if current_step != "payment":
            return redirect(reverse("order"))

        order_data = request.session.get("order_data")
        order_department = request.session.get("order_department")
        cart_items, total = sync_get_cart_items(request)
        categories = Category.objects.all()

        item_name = "Order from cashyong"
        paypal_dict = {
            "business": os.environ.get("PAYPAL_BUSINESS"),
            "amount": total,
            "currency_code": "USD",
            "item_name": item_name,
            "invoice": str(item_name),
            "notify_url": request.build_absolute_uri(reverse("paypal-ipn")),
            "return_url": request.build_absolute_uri(reverse("store:cart")),
            "cancel_return": request.build_absolute_uri(reverse("payment")) + "?cancel=1&custom={}".format(item_name),
        }

        payment_form = PayPalPaymentsForm(initial=paypal_dict)

        cart_items_data = []
        for item in cart_items:
            product = item["product"]
            product_data = {
                "id": product.id,
                "category": product.category.title,
                "title": product.title,
                "price": str(product.price),
                "photo1": product.photo1.url
            }
            cart_items_data.append({"product": product_data, "quantity": item["quantity"],
                                    "subtotal": str(item["subtotal"])})

        if order_data:
            name = order_data.get("name")
            surname = order_data.get("surname")
            email = order_data.get("email")
            phone_number = order_data.get("phone_number")
            city = order_data.get("city")
            department = order_department.get("department")
            description = order_department.get("description")
            # send_order_email_task.delay(
            #     total,
            #     cart_items_data,
            #     name=name,
            #     surname=surname,
            #     email=email,
            #     phone_number=phone_number,
            #     city=city,
            #     department=department,
            #     description=description,
            # )
            # send_order_email(email=email, description=description, total=total, cart_items=cart_items, name=name,
            #                  surname=surname, phone_number=phone_number, city=city, department=department)
            # send_order_client_email(cart_items=cart_items, name=name, email=email, department=department, city=city)

        return render(
            request, "payment.html",
            {"total": total, "payment_form": payment_form, "cart_items": cart_items_data, "categories": categories}
        )

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        ipn_obj = request.POST
        if ipn_obj.get("txn_type") == "web_accept" and ipn_obj.get("payment_status") == "Completed":
            # Done payment
            cart_items, total = sync_get_cart_items(ipn_obj.get("invoice"))
            # item_name = "Order from cashyong"
            # send_order_email_task.delay(str(total), str(cart_items))

        return HttpResponse(status=200)


class OrderWorldwide(TemplateView, FormView):
    http_method_names = ["get", "post"]
    form_class = OrderWorldwideForm
    template_name = "order_worldwide.html"
    success_url = "/department/worldwide/"

    def get(self, request, *args, **kwargs):
        cart_items, total = sync_get_cart_items(request)
        form_data = request.session.get("order_data_worldwide")
        if form_data:
            form = self.form_class(initial=form_data)
        else:
            form = self.form_class()
        return render(request, "order_worldwide.html", {"total": total, "cart_items": cart_items, "form": form})

    def form_valid(self, form):
        name = form.cleaned_data["name"]
        surname = form.cleaned_data["surname"]
        email = form.cleaned_data["email"]
        phone_number = form.cleaned_data["phone_number"]
        country = form.cleaned_data["country"]

        self.request.session["order_data_worldwide"] = {
            "name": name,
            "surname": surname,
            "email": email,
            "phone_number": str(phone_number),
            "country": country,
        }
        self.request.session["current_step_worldwide"] = "department_worldwide"

        return redirect(self.success_url)

    def form_invalid(self, form):
        cart_items, total = sync_get_cart_items(self.request)
        return self.render_to_response(self.get_context_data(form=form, cart_items=cart_items, total=total))


class DepartmentWorldwide(TemplateView, FormView):
    http_method_names = ["get", "post"]
    form_class = DepartmentWorldwideForm
    template_name = "department_worldwide.html"
    success_url = "payment_worldwide"

    def get(self, request, *args, **kwargs):
        current_step = request.session.get("current_step_worldwide")
        if current_step != "department_worldwide":
            return redirect(reverse("order_worldwide"))

        cart_items, total = sync_get_cart_items(request)
        order_data = request.session.get("order_data_worldwide")
        form = self.form_class(initial=order_data)

        return render(request, "department_worldwide.html", {"total": total, "cart_items": cart_items, "form": form})

    def form_valid(self, form):
        current_step = self.request.session.get("current_step_worldwide")
        if current_step != "department_worldwide":
            return HttpResponse(status=403)

        city = form.cleaned_data["city"]
        description = form.cleaned_data["description"]
        street = form.cleaned_data["street"]
        delivery_service = form.cleaned_data["delivery_service"]
        self.request.session["order_department_worldwide"] = {
            "department": city,
            "description": description,
            "street": street,
            "delivery_service": delivery_service
        }

        self.request.session["current_step_worldwide"] = "payment_worldwide"

        return redirect(self.success_url)


class PaymentWorldwide(TemplateView, FormView):
    http_method_names = ["get", "post"]

    @csrf_exempt
    def get(self, request, *args, **kwargs):
        current_step = request.session.get("current_step_worldwide")
        if current_step != "payment_worldwide":
            return redirect(reverse("order_worldwide"))

        order_data = request.session.get("order_data_worldwide")
        order_department = request.session.get("order_department_worldwide")
        cart_items, total = sync_get_cart_items(request)
        categories = Category.objects.all()

        item_name = "Order from cashyong"
        paypal_dict = {
            "business": os.environ.get("PAYPAL_BUSINESS"),
            "amount": total,
            "currency_code": "USD",
            "item_name": item_name,
            "invoice": str(item_name),
            "notify_url": request.build_absolute_uri(reverse("paypal-ipn")),
            "return_url": request.build_absolute_uri(reverse("store:cart")),
            "cancel_return": request.build_absolute_uri(reverse("payment")) + "?cancel=1&custom={}".format(item_name),
        }

        payment_form = PayPalPaymentsForm(initial=paypal_dict)

        cart_items_data = []
        for item in cart_items:
            product = item["product"]
            product_data = {
                "id": product.id,
                "category": product.category.title,
                "title": product.title,
                "price": str(product.price),
                "photo1": product.photo1.url
            }
            cart_items_data.append({"product": product_data, "quantity": item["quantity"],
                                    "subtotal": str(item["subtotal"])})

        if order_data:
            name = order_data.get("name")
            surname = order_data.get("surname")
            email = order_data.get("email")
            phone_number = order_data.get("phone_number")
            country = order_data.get("country")
            city = order_department.get("city")
            street = order_department.get("street")
            delivery_service = order_department.get("delivery_service")
            description = order_department.get("description")
            # send_order_email(email=email, description=description, total=total, cart_items=cart_items, name=name,
            #                  surname=surname, phone_number=phone_number, city=city, department=department)
            # send_order_client_email(cart_items=cart_items, name=name, email=email, department=department, city=city)

        return render(
            request, "payment_worldwide.html",
            {"total": total, "payment_form": payment_form, "cart_items": cart_items_data, "categories": categories}
        )

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        ipn_obj = request.POST
        if ipn_obj.get("txn_type") == "web_accept" and ipn_obj.get("payment_status") == "Completed":
            # Done payment
            cart_items, total = sync_get_cart_items(ipn_obj.get("invoice"))
            # item_name = "Order from cashyong"
            # send_order_email_task.delay(str(total), str(cart_items))

        return HttpResponse(status=200)


@receiver(valid_ipn_received)
def payment_notification(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.get("txn_type") == "web_accept" and ipn_obj.get("payment_status") == "Completed":
        # Done payment
        cart_items, total = sync_get_cart_items(ipn_obj.get("invoice"))
        # item_name = "Order from cashyong"
        # send_order_email_task.delay(str(total), str(cart_items))
