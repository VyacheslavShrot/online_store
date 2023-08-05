from django.db import models


class BaseModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(null=True, auto_now_add=True)
    modified_at = models.DateTimeField(null=True, auto_now_add=True)


class ImageModel(models.Model):
    class Meta:
        abstract = True

    photo1 = models.ImageField(upload_to="images/", blank=True, null=False)
    photo2 = models.ImageField(upload_to="images/", blank=True, null=True)
    photo3 = models.ImageField(upload_to="images/", blank=True, null=True)
    photo4 = models.ImageField(upload_to="images/", blank=True, null=True)
    photo5 = models.ImageField(upload_to="images/", blank=True, null=True)
    photo6 = models.ImageField(upload_to="images/", blank=True, null=True)
