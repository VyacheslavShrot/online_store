from django.contrib.auth import get_user_model
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from api.serializers import (ArchiveBaseSerializer, CategoryBaseSerializer,
                             ProductBaseSerializer, ProductCreateSerializer,
                             ProductUpdateSerializer, UserSerializer)
from core.permissions import IsSuperUser
from store.models import Archive, Category, Product


class UserViewSet(ModelViewSet):
    permission_classes = (IsSuperUser,)
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class ProductDetailView(RetrieveAPIView):
    serializer_class = ProductBaseSerializer

    def get_object(self):
        return Product.objects.get(id=self.kwargs.get("id"))


class ProductListView(ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Product.objects.all()
    serializer_class = ProductBaseSerializer


class ProductCreateView(CreateAPIView):
    permission_classes = (IsSuperUser,)
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer


class ProductUpdateView(UpdateAPIView):
    permission_classes = (IsSuperUser,)
    serializer_class = ProductUpdateSerializer

    def get_object(self):
        return Product.objects.get(id=self.kwargs.get("id"))


class ProductDeleteView(DestroyAPIView):
    permission_classes = (IsSuperUser,)
    serializer_class = ProductBaseSerializer

    def get_object(self):
        return Product.objects.get(id=self.kwargs.get("id"))


class CategoryListView(ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Category.objects.all()
    serializer_class = CategoryBaseSerializer


class CategoryCreateView(CreateAPIView):
    permission_classes = (IsSuperUser,)
    queryset = Category.objects.all()
    serializer_class = CategoryBaseSerializer


class CategoryUpdateView(UpdateAPIView):
    permission_classes = (IsSuperUser,)
    serializer_class = CategoryBaseSerializer

    def get_object(self):
        return Category.objects.get(id=self.kwargs.get("id"))


class CategoryDeleteView(DestroyAPIView):
    permission_classes = (IsSuperUser,)
    serializer_class = CategoryBaseSerializer

    def get_object(self):
        return Category.objects.get(id=self.kwargs.get("id"))


class ArchiveListView(ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Archive.objects.all()
    serializer_class = ArchiveBaseSerializer


class ArchiveCreateView(CreateAPIView):
    permission_classes = (IsSuperUser,)
    queryset = Archive.objects.all()
    serializer_class = ArchiveBaseSerializer


class ArchiveUpdateView(UpdateAPIView):
    permission_classes = (IsSuperUser,)
    serializer_class = ArchiveBaseSerializer

    def get_object(self):
        return Archive.objects.get(id=self.kwargs.get("id"))


class ArchiveDeleteView(DestroyAPIView):
    permission_classes = (IsSuperUser,)
    serializer_class = ArchiveBaseSerializer

    def get_object(self):
        return Archive.objects.get(id=self.kwargs.get("id"))
