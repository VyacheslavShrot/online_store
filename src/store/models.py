from django.db import models

from core.models import BaseModel, ImageModel


class Product(BaseModel, ImageModel):
    category = models.ForeignKey(
        to="store.Category", related_name="products", blank=True, null=True, on_delete=models.CASCADE
    )
    title = models.CharField(max_length=120)
    size = models.CharField(max_length=5, default="*")
    width = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    height = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    depth = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    characteristic = models.TextField(max_length=1024, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=10, default=0)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "All Products"

    def __str__(self):
        return f"({self.id}) {self.category.title} {self.title} {self.price}"

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def products_count(self):
        return Product.objects.count()


class Category(models.Model):
    title = models.CharField(max_length=30, default="Other")

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "All Category"

    def __str__(self):
        return f"{self.title}"


class Archive(BaseModel, ImageModel):
    SOLD_OUT = "SOLD OUT"
    title = models.CharField(max_length=120)
    characteristic = models.TextField(max_length=1024, blank=True)
    status = models.CharField(max_length=120, default=SOLD_OUT)

    class Meta:
        verbose_name = "Archive"
        verbose_name_plural = "All Archive"

    def __str__(self):
        return f"({self.id}) {self.title} {self.characteristic}"

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def archive_count(self):
        return Archive.objects.count()
