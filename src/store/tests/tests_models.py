from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from core.utils.samples import sample_archive, sample_product
from store.models import Archive, Product


class TestStoreModel(TestCase):
    def setUp(self) -> None:
        self.archive = Archive.objects.create(title="archive")
        self.product = Product.objects.create(title="product")
        self.test_product = sample_product(title="product")
        self.test_archive = sample_archive(title="archive")

    def tearDown(self) -> None:
        self.archive.delete()
        self.product.delete()
        self.test_product.delete()
        self.test_archive.delete()

    def test_product_title_is_correct(self):
        self.assertEqual(self.product.title, self.test_product.title)

    def test_archive_title_is_correct(self):
        self.assertEqual(self.archive.title, self.test_archive.title)

    def test_product_title_exceeds_limit_raises_error(self):
        with self.assertRaises(ValidationError):
            sample_product(title="G" * 1000)

    def test_archive_title_exceeds_limit_raises_error(self):
        with self.assertRaises(ValidationError):
            sample_archive(title="G" * 1000)
