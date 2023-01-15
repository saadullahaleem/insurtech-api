from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db.models import Count
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from core.api.filters import CustomerFilter, PolicyFilter
from core.api.v1.serializers import CustomerSerializer, PolicySerializer
from core.models import Policy

from democranceapi.permissions import IsCustomer

User = get_user_model()


class CustomerViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsAdminUser, )
    filterset_class = CustomerFilter

    def get_serializer_class(self):
        return CustomerSerializer

    def get_queryset(self):
        return User.objects.filter(is_customer=True).prefetch_related(
            "policies").annotate(policies_count=Count("policies")).order_by(
            "-date_joined")

    @action(detail=True, methods=["PUT"])
    def set_password(self, request, pk, *args, **kwargs):
        password = request.data.get("password")
        try:
            validate_password(password)
        except ValidationError as e:
            return Response({
                "errors": e
            }, status=status.HTTP_400_BAD_REQUEST)

        user = self.get_object()
        user.set_password(password)
        user.save()
        return Response({
            "message": "Password set successfully"
        }, status=status.HTTP_200_OK)


class PolicyViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, (IsAdminUser | IsCustomer),)
    filterset_class = PolicyFilter

    def get_queryset(self):
        qs = Policy.objects.select_related("customer")
        if getattr(self.request.user, 'is_customer', False):
            qs = Policy.objects.filter(customer=self.request.user)

        return qs.order_by('-created')

    def get_serializer_class(self):
        return PolicySerializer

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

    @action(detail=True, methods=["PUT"])
    def activate(self, request, pk, *args, **kwargs):
        policy = self.get_object()
        if policy.is_active:
            return Response({
                "errors": "Policy already active"
            }, status=status.HTTP_400_BAD_REQUEST)

        policy.activate()

        return Response({
            "message": "Policy successfully activated"
        })
