from datetime import datetime

from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import RedirectView, TemplateView
from webargs import fields
from webargs.djangoparser import use_kwargs

from store.models import Archive, Category, Product


class StoreView(TemplateView):
    template_name = "store.html"
    http_method_names = ["get"]

    @use_kwargs(
        {
            "title": fields.Str(required=False),
            "search_text": fields.Str(required=False),
        },
        location="query",
    )
    def get(self, request, **kwargs):
        products = Product.objects.all()
        categories = Category.objects.all()
        cart_items, total = get_cart_items(request)

        sort_by = request.GET.get("sort_by", "")
        if sort_by == "-price":
            products = products.order_by("-price")
        elif sort_by == "price":
            products = products.order_by("price")

        search_fields = [
            "title",
        ]

        search_text = kwargs.get("search_text", "")
        if search_text:
            request.session[f"search_text_{datetime.now()}"] = search_text

            or_filter = Q()

            for field in search_fields:
                # accumulate filter condition
                or_filter |= Q(**{f"{field}__contains": search_text})

            products = products.filter(or_filter)
        else:
            request.session.pop("search_text", "")

        for field_name, field_value in kwargs.items():
            if field_name == "search_text":
                continue

            if field_value:
                products = products.filter(**{field_name: field_value})

        return render(
            request,
            template_name="store.html",
            context={
                "products": products,
                "categories": categories,
                "sort_by": sort_by,
                "cart_items": cart_items,
                "total": total,
                "search_text": search_text,
            },
        )


class ProductCategoryView(TemplateView):
    template_name = "product_category.html"
    http_method_names = ["get"]

    @use_kwargs(
        {
            "title": fields.Str(required=False),
            "search_text": fields.Str(required=False),
        },
        location="query",
    )
    def get(self, request, id, **kwargs):
        products = Product.objects.filter(category=id)
        all_category = Category.objects.all()
        categories = get_object_or_404(Category.objects.all(), id=id)
        cart_items, total = get_cart_items(request)

        sort_by = request.GET.get("sort_by", "")
        if sort_by == "-price":
            products = products.order_by("-price")
        elif sort_by == "price":
            products = products.order_by("price")

        search_fields = [
            "title",
        ]

        search_text = kwargs.get("search_text", "")
        if search_text:
            request.session[f"search_text_{datetime.now()}"] = search_text

            or_filter = Q()

            for field in search_fields:
                # accumulate filter condition
                or_filter |= Q(**{f"{field}__contains": search_text})

            products = products.filter(or_filter)
        else:
            request.session.pop("search_text", "")

        for field_name, field_value in kwargs.items():
            if field_name == "search_text":
                continue

            if field_value:
                products = products.filter(**{field_name: field_value})

        return render(
            request,
            template_name="product_category.html",
            context={
                "products": products,
                "categories": categories,
                "all_category": all_category,
                "sort_by": sort_by,
                "cart_items": cart_items,
                "total": total,
                "search_text": search_text,
            },
        )


class ProductView(TemplateView):
    template_name = "product.html"
    http_method_names = ["get"]

    def get(self, request, id):
        categories = Category.objects.all()
        products = get_object_or_404(Product.objects.all(), id=id)
        product_like = Product.objects.filter(category=products.category)[:3]
        cart_items, total = get_cart_items(request)

        return render(
            request,
            template_name="product.html",
            context={
                "products": products,
                "product_like": product_like,
                "categories": categories,
                "cart_items": cart_items,
                "total": total,
            },
        )


class ArchiveView(TemplateView):
    template_name = "archive.html"
    http_method_names = ["get"]

    def get(self, request):
        archives = Archive.objects.all()
        all_category = Category.objects.all()
        cart_items, total = get_cart_items(request)

        return render(
            request,
            template_name="archive.html",
            context={"archives": archives, "all_category": all_category, "cart_items": cart_items, "total": total},
        )


class AddToCart(RedirectView):
    def get(self, request, product_id, *args, **kwargs):
        product = get_object_or_404(Product, id=product_id)
        cart = request.session.get("cart", {})
        if str(product_id) in cart:
            """
            FOR MORE THEN 1 QUANTITY !!!
            """
            # cart[str(product_id)]['quantity'] += 1
            messages.error(request, "item is already in the cart")
        else:
            cart[str(product_id)] = {"quantity": 1}
            messages.success(request, "Item added to cart")
        request.session["cart"] = cart
        url = reverse("store:product", args=[product.id])
        return redirect(url)


class RemoveFromCart(RedirectView):
    def get(self, request, product_id, *args, **kwargs):
        product = get_object_or_404(Product, id=product_id)
        cart = request.session.get("cart", {})
        if str(product.id) in cart:
            del cart[str(product.id)]
            request.session["cart"] = cart
        url = reverse("store:cart")
        return redirect(url)


def get_cart_items(request):
    cart = request.session.get("cart", {})
    cart_items = []
    total = 0
    for product_id, item in cart.items():
        product = get_object_or_404(Product, id=product_id)
        quantity = item["quantity"]
        subtotal = product.price * quantity
        total += subtotal
        cart_items.append({"product": product, "quantity": quantity, "subtotal": subtotal})
    return cart_items, total


class Cart(TemplateView):
    def get(self, request, *args, **kwargs):
        cart_items, total = get_cart_items(request)
        categories = Category.objects.all()

        return render(request, "cart.html", {"cart_items": cart_items, "total": total, "categories": categories})
