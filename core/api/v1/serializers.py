from django.db import transaction
from rest_framework import serializers

from core.models import Profile, User, Policy


class CustomChoiceField(serializers.ChoiceField):
    def to_representation(self, value):
        choice = self.choice_strings_to_values.get(value)
        if choice:
            return choice.label


class ProfileSerializer(serializers.ModelSerializer):
    date_of_birth = serializers.DateField()

    class Meta:
        model = Profile
        fields = ("date_of_birth", "personal_identification")


class CustomerSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        with transaction.atomic():
            profile_payload = validated_data.pop("profile")
            profile = Profile.objects.create(**profile_payload)
            customer = User.objects.create(
                profile=profile, is_customer=True, **validated_data)
        return customer

    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email", "profile",
                  "password")


class PolicySerializer(serializers.ModelSerializer):
    state = CustomChoiceField(Policy.State)
    customer = CustomerSerializer(read_only=True)

    class Meta:
        model = Policy
        fields = ('id', 'customer', 'premium', 'cover', 'state')
