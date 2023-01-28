import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.models import Policy
from tests.factories import UserFactory, ProfileFactory, PolicyFactory


class CustomerViewSetTest(APITestCase):
    def setUp(self):
        self.customer = UserFactory(is_customer=True).create()
        self.profile = ProfileFactory(user=self.customer).create()
        self.url = reverse("customers-list")
        self.admin = UserFactory(is_staff=True).create()
        self.client.force_authenticate(user=self.admin)

    def test_list_customers(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["email"],
                         self.customer.email)

    def test_set_password(self):
        new_password = "new_password"
        response = self.client.put(
            f"{self.url}{self.customer.id}/set_password/",
            data=json.dumps({"password": new_password}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "Password set successfully")
        self.client.logout()
        self.client.login(username=self.customer.username,
                          password=new_password)


class PolicyViewSetTest(APITestCase):
    def setUp(self):
        self.admin = UserFactory(is_staff=True).create()
        self.customer = UserFactory(is_customer=True).create()
        self.policy = PolicyFactory(customer=self.customer).create()
        self.policy2 = PolicyFactory(customer=self.customer).create()

    def test_list_policies_authenticated(self):
        self.client.force_authenticate(self.admin)
        response = self.client.get(reverse('quotes-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_policies_unauthenticated(self):
        response = self.client.get(reverse('quotes-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_policy_authenticated(self):
        self.client.force_authenticate(self.admin)
        data = json.dumps({'state': 'NW', 'premium': 10, 'cover':
            100})
        response = self.client.post(reverse('quotes-list'), data,
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Policy.objects.count(), 3)

    def test_create_policy_unauthenticated(self):
        data = json.dumps({'name': 'test policy', 'price': 10})
        response = self.client.post(reverse('quotes-list'), data,
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_policy_authenticated(self):
        self.client.force_authenticate(self.admin)
        response = self.client.get(
            reverse('quotes-detail', args=[self.policy.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['premium'], self.policy.premium)
        self.assertEqual(response.data['cover'], self.policy.cover)

    def test_retrieve_policy_unauthenticated(self):
        response = self.client.get(
            reverse('quotes-detail', args=[self.policy.id]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_policy_authenticated(self):
        self.client.force_authenticate(self.admin)
        data = json.dumps({'name': 'updated policy', 'premium': 20})
        response = self.client.patch(
            reverse('quotes-detail', args=[self.policy.id]), data,
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.policy.refresh_from_db()
        self.assertEqual(self.policy.premium, 20)

    def test_update_policy_unauthenticated(self):
        data = json.dumps({'name': 'updated policy', 'price': 20})
        response = self.client.put(
            reverse('quotes-detail', args=[self.policy.id]), data,
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
