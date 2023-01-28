from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.exceptions import ValidationError

from core.api.v1.serializers import CustomerSerializer
from core.models import Profile
from tests.factories import UserFactory, ProfileFactory

User = get_user_model()


class CustomerSerializerTest(TestCase):

    def setUp(self):
        self.profile = ProfileFactory().prepare()
        self.user = UserFactory(is_customer=True,
                                profile=self.profile).prepare()
        self.customer_data = {
            'email': self.user.email,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'password': 'secretpassword',
            'policies_count': 0,
            'profile': {
                'date_of_birth': self.profile.date_of_birth,
                'personal_identification': self.profile.personal_identification,
            }
        }
        self.customer_serializer = CustomerSerializer(data=self.customer_data)

    def test_invalid_data_raises_exception(self):
        self.customer_data['email'] = 'invalidemail'
        self.customer_serializer = CustomerSerializer(data=self.customer_data)
        with self.assertRaises(ValidationError):
            self.customer_serializer.is_valid(raise_exception=True)

    def test_correct_data_is_validated(self):
        self.assertTrue(self.customer_serializer.is_valid())

    def test_create(self):
        self.assertTrue(self.customer_serializer.is_valid())
        self.customer_serializer.save()
        self.assertEqual(User.objects.filter(email=self.user.email).count(), 1)
        self.assertEqual(Profile.objects.filter(
            user__email=self.user.email).count(), 1)

    def test_serialized_data_with_policies_count(self):
        self.user.policies_count = 1
        self.customer_serializer = CustomerSerializer(self.user)
        serialized_data = self.customer_serializer.data
        self.assertEqual(serialized_data['policies_count'], 1)

    def test_serialized_data(self):
        self.assertTrue(self.customer_serializer.is_valid())
        serialized_data = self.customer_serializer.data
        del self.customer_data['password']
        del self.customer_data['policies_count']
        self.customer_data['profile'][
            'date_of_birth'] = self.profile.date_of_birth.strftime('%Y-%m-%d')
        serialized_data['profile'] = dict(serialized_data['profile'])
        self.assertDictEqual(dict(serialized_data), self.customer_data)
