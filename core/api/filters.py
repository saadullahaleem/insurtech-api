from django_filters import rest_framework as filters
from django.contrib.auth import get_user_model

from core.models import Policy

User = get_user_model()


class CustomerFilter(filters.FilterSet):
    policy_state = filters.ChoiceFilter(field_name="policies__state",
                                      choices=Policy.State.choices)
    date_of_birth = filters.IsoDateTimeFilter(
        field_name="profile__date_of_birth")
    policies_count_gt = filters.NumberFilter(field_name='policies_count',
                                     lookup_expr='gt')
    policies_count_lt = filters.NumberFilter(field_name='policies_count',
                                     lookup_expr='lt')
    policies_count_gte = filters.NumberFilter(field_name='policies_count',
                                     lookup_expr='gte')
    policies_count_lte = filters.NumberFilter(field_name='policies_count',
                                     lookup_expr='lte')

    class Meta:
        model = User
        fields = {
            'first_name': ['icontains'],
            'last_name': ['icontains'],
        }


class PolicyFilter(filters.FilterSet):
    state = filters.ChoiceFilter(field_name="policies__state",
                                      choices=Policy.State.choices)

    class Meta:
        model = Policy
        fields = {
            'cover': ['gt', 'lt', 'gte', 'lte', 'exact'],
            'premium': ['gt', 'lt', 'gte', 'lte', 'exact'],
        }