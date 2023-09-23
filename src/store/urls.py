from django.urls import path

from store.views import (AddToCart, ArchiveView, Cart, ProductCategoryView,
                         ProductView, RemoveFromCart, StoreView)

app_name = "store"

urlpatterns = [
    path("", StoreView.as_view(), name="store"),
    path("category/<int:id>/", ProductCategoryView.as_view(), name="category"),
    path("archive/", ArchiveView.as_view(), name="archive"),
    path("product/<int:product_id>/", ProductView.as_view(), name="product"),
    path("add-to-cart/<int:product_id>/", AddToCart.as_view(), name="add_to_cart"),
    path("remove-from-cart/<int:product_id>/", RemoveFromCart.as_view(), name="remove_from_cart"),
    path("cart/", Cart.as_view(), name="cart"),
]
