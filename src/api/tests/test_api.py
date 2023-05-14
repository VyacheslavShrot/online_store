from collections import OrderedDict

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from core.utils.samples import sample_archive, sample_product
from store.models import Category


class TestAPI(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

        self.product = sample_product(title="Polar Sweatpants", price=100)

        self.archive = sample_archive(title="DC Shoes", characteristic="Some text")

        self.user = get_user_model().objects.create(username="test_api")
        self.user.set_password("123456789")
        self.user.save()

        self.admin = get_user_model().objects.create_superuser(username="admin", is_staff=True)
        self.admin.set_password("123456789")
        self.admin.save()

    def test_product_detail(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("api:product_details", kwargs={"id": self.product.id}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data,
            {
                "id": 1,
                "category": {"id": 1, "title": "Other"},
                "title": "Polar Sweatpants",
                "price": "100.00",
                "products_count": 1,
            },
        )

    def test_product_detail_no_access(self):
        response = self.client.get(reverse("api:product_details", kwargs={"id": self.product.id}))

        self.assertEqual(response.status_code, 401)

    def test_archive_list(self):
        response = self.client.get(reverse("api:archive_list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [{"id": 1, "title": "DC Shoes", "status": "SOLD OUT", "archive_count": 1}])

    def test_product_create(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(reverse("api:product_create"), data={"category": 1, "title": "Test"})

        self.assertEqual(response.status_code, 201)

    def test_product_update(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.put(
            reverse("api:product_update", kwargs={"id": self.product.id}), data={"title": "Test"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"title": "Test", "price": "100.00", "size": "*", "products_count": 1})
