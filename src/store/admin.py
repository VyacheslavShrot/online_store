from django.contrib import admin

from store.models import Archive, Category, Product

admin.site.register([Category])


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["category", "title", "size", "price"]

    list_display_links = ["category", "title", "size", "price"]

    list_filter = ["size", "category"]


@admin.register(Archive)
class ArchiveAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "status",
    ]

    list_display_links = [
        "title",
        "status",
    ]
