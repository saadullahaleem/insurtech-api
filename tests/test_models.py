import faker

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.exceptions import ValidationError

from tests.factories import UserFactory, ProfileFactory, PolicyFactory

User = get_user_model()
fake = faker.Faker()


class UserModelTest(TestCase):

    def test_model_configuration(self):
        self.assertEqual(User.USERNAME_FIELD, 'email')
        self.assertIn('username', User.REQUIRED_FIELDS)

    def test_email_is_unique(self):
        email = fake.email()
        UserFactory(email=email).create()
        with self.assertRaises(ValidationError):
            UserFactory(email=email).create()

    def test_email_validation(self):
        with self.assertRaises(ValidationError):
            UserFactory(email='invalid_email').create()

    def test_email_max_length_validation(self):
        with self.assertRaises(ValidationError):
            invalid_email = "a" * 256 + "@example.com"
            UserFactory(email=invalid_email).create()

    def test_save_method(self):
        email = fake.email()
        user = UserFactory(email=email).create()
        self.assertTrue(user.username.startswith(email.split("@")[0]))

    def test_str_method(self):
        user = User()
        self.assertEqual(str(user), user.email)

    def test_one_to_one_field(self):
        user = UserFactory().create()
        profile = ProfileFactory(user=user).create()
        self.assertEqual(user.profile, profile)

    def test_is_customer_field(self):
        user = UserFactory().create()
        self.assertEqual(user.is_customer, False)


class PolicyTestCase(TestCase):
    def test_activate(self):
        policy = PolicyFactory().create()
        policy.activate()
        self.assertTrue(policy.is_active)

    def test_str_method(self):
        policy = PolicyFactory().create()
        self.assertEqual(str(policy), f"{policy.customer.email}-{policy.premium}-{policy.state}")