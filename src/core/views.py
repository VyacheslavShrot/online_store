from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView

from core.forms import ReportForm
from core.services.emails import send_report_email, send_client_report_email
# from core.tasks import send_report_email_task
from store.models import Category
from store.views import async_get_cart_items, sync_get_cart_items


class IndexView(TemplateView):
    template_name = "index.html"
    http_method_names = ["get"]

    async def get(self, request, *args, **kwargs):
        cart_items, total = await async_get_cart_items(request)
        categories = []

        async for category in Category.objects.all():
            categories.append(category)

        return render(
            request, "index.html", context={"cart_items": cart_items, "total": total, "categories": categories}
        )


class SupportView(TemplateView):
    template_name = "support.html"
    http_method_names = ["get"]

    async def get(self, request, *args, **kwargs):
        cart_items, total = await async_get_cart_items(request)
        return render(request, "support.html", context={"cart_items": cart_items, "total": total})


class ReportView(TemplateView, FormView):
    template_name = "report.html"
    http_method_names = ["get", "post"]
    form_class = ReportForm
    success_url = "/report/"

    def get(self, request, *args, **kwargs):
        cart_items, total = sync_get_cart_items(request)
        form_data = request.session.get("report_data")
        order_email_data = request.session.get("order_data")
        if form_data:
            form = self.form_class(initial=form_data)
        elif order_email_data:
            form = self.form_class(initial=order_email_data)
        else:
            form = self.form_class()

        return render(request, "report.html", context={"form": form, "cart_items": cart_items, "total": total})

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        description = form.cleaned_data["description"]

        self.request.session["report_data"] = {
            "email": email,
        }
        messages.success(self.request, 'Report of your problem was sending')
        # send_report_email_task.delay(email=email, description=description)
        send_report_email(email=email, description=description)
        send_client_report_email(email=email, description=description)
        return redirect(self.success_url)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
