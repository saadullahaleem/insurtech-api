from django.contrib.auth import get_user_model
from faker import Faker
from model_bakery import baker

from core.models import Profile, Policy

User = get_user_model()

faker = Faker()


class UserFactory:
    def __init__(self, email=None, is_customer=False, profile=None,
                 is_staff=False, first_name=None, last_name=None):
        self.email = email or faker.email()
        self.first_name = first_name or faker.first_name()
        self.last_name = last_name or faker.last_name()
        self.is_customer = is_customer
        self.profile = profile
        self.is_staff = is_staff

    def create(self):
        return baker.make(User, email=self.email, is_customer=self.is_customer,
                          profile=self.profile, is_staff=self.is_staff,
                          first_name=self.first_name, last_name=self.last_name)

    def prepare(self):
        return baker.prepare(User, email=self.email,
                             is_customer=self.is_customer,
                             profile=self.profile, is_staff=self.is_staff,
                             first_name=self.first_name,
                             last_name=self.last_name)

    def create_batch(self, size):
        return baker.make_batch(User, size, email=self.email,
                                is_customer=self.is_customer,
                                profile=self.profile)


class ProfileFactory:
    def __init__(self, date_of_birth=None, personal_identification=None,
                 user=None):
        self.date_of_birth = date_of_birth or faker.date_of_birth()
        self.personal_identification = personal_identification or faker.ssn()
        self.user = user

    def create(self):
        return baker.make(Profile, date_of_birth=self.date_of_birth,
                          personal_identification=self.personal_identification,
                          user=self.user)

    def prepare(self):
        return baker.prepare(Profile, date_of_birth=self.date_of_birth,
                             personal_identification=self.personal_identification,
                             user=self.user)


class PolicyFactory:
    def __init__(self, customer=None, premium=None, cover=None, state=None):
        self.customer = customer
        self.premium = premium or faker.random_int(min=100, max=1000)
        self.cover = cover or faker.random_int(min=10000, max=100000)
        self.state = state or Policy.State.NEW

    def create(self):
        if self.customer is None:
            self.customer = UserFactory().create()
        return baker.make(Policy, customer=self.customer, premium=self.premium,
                          cover=self.cover, state=self.state)
