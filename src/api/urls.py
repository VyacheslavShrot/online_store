from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers

from api.views import (ArchiveCreateView, ArchiveDeleteView, ArchiveListView,
                       ArchiveUpdateView, CategoryCreateView,
                       CategoryDeleteView, CategoryListView,
                       CategoryUpdateView, ProductCreateView,
                       ProductDeleteView, ProductDetailView, ProductListView,
                       ProductUpdateView, UserViewSet)

app_name = "api"
router = routers.DefaultRouter()
router.register("user", UserViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="Store API",
        default_version="v1",
        description="API for passing products",
        term_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(name="sle3pinhood"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include("djoser.urls.jwt")),
    path("docs/", schema_view.with_ui("redoc", cache_timeout=0), name="swagger_docs"),
    path("product/<int:id>/", ProductDetailView.as_view(), name="product_details"),
    path("product/", ProductListView.as_view(), name="product_list"),
    path("product/create/", ProductCreateView.as_view(), name="product_create"),
    path("product/update/<int:id>/", ProductUpdateView.as_view(), name="product_update"),
    path("product/delete/<int:id>/", ProductDeleteView.as_view(), name="product_delete"),
    path("category/", CategoryListView.as_view(), name="category_list"),
    path("category/create/", CategoryCreateView.as_view(), name="category_create"),
    path("category/update/<int:id>/", CategoryUpdateView.as_view(), name="category_update"),
    path("category/delete/<int:id>/", CategoryDeleteView.as_view(), name="category_delete"),
    path("archive/", ArchiveListView.as_view(), name="archive_list"),
    path("archive/create/", ArchiveCreateView.as_view(), name="archive_create"),
    path("archive/update/<int:id>/", ArchiveUpdateView.as_view(), name="archive_update"),
    path("archive/delete/<int:id>/", ArchiveDeleteView.as_view(), name="archive_delete"),
]
