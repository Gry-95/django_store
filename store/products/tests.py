from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from products.models import Product, ProductCategory


class ProductsListViewTestCase(TestCase):
    fixtures = ['category.json', 'goods.json']

    def setUp(self):
        self.products = Product.objects.all()

    def test_list(self):
        path = reverse('products')
        response = self.client.get(path)
        self._comon_tests(response)
        self.assertEqual(list(response.context_data['object_list']), list(self.products[:6]))

    def test_list_with_category(self):
        category = ProductCategory.objects.first()
        path = reverse('category', kwargs={'category_id': category.id})
        response = self.client.get(path)
        self._comon_tests(response)
        self.assertEqual(
            list(response.context_data['object_list']),
            list(self.products.filter(category_id=category.id)[:6]))

    def _comon_tests(self, response):
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Каталог')
        self.assertTemplateUsed(response, 'products/product_list.html')
