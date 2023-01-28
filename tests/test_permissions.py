from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from democranceapi.permissions import IsCustomer
from tests.factories import UserFactory


class IsCustomerPermissionTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory(is_customer=True).create()
        self.url = reverse("customers-list")

    def test_has_permission(self):
        request = self.client.get(self.url)
        request.user = self.user
        permission = IsCustomer()
        self.assertTrue(permission.has_permission(request, None))

    def test_has_no_permission(self):
        request = self.client.get(self.url)
        self.user.is_customer = False
        self.user.save()
        request.user = self.user
        permission = IsCustomer()
        self.assertFalse(permission.has_permission(request, None))