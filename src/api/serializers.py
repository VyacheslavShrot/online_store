from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

from store.models import Archive, Category, Product


class UserSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "email", "is_staff")


class CategoryBaseSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "title",
        )


class ProductBaseSerializer(ModelSerializer):
    category = CategoryBaseSerializer()

    class Meta:
        model = Product
        fields = ("id", "category", "title", "price", "products_count")


class ProductCreateSerializer(ProductBaseSerializer):
    category = "*"

    class Meta:
        model = Product
        fields = ("category", "title", "price", "products_count")


class ProductUpdateSerializer(ProductBaseSerializer):
    class Meta:
        model = Product
        fields = ("title", "price", "size", "products_count")


class ArchiveBaseSerializer(ModelSerializer):
    class Meta:
        model = Archive
        fields = ("id", "title", "status", "archive_count")
