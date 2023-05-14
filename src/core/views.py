from django.shortcuts import render
from django.views.generic import TemplateView

from store.models import Category
from store.views import get_cart_items


class IndexView(TemplateView):
    template_name = "index.html"
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        cart_items, total = get_cart_items(request)
        categories = Category.objects.all()
        return render(
            request, "index.html", context={"cart_items": cart_items, "total": total, "categories": categories}
        )
