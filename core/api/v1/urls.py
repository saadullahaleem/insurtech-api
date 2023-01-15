from rest_framework.routers import DefaultRouter

from core.api.v1.views import CustomerViewSet, PolicyViewSet

router = DefaultRouter()
router.register('customers', CustomerViewSet, basename="customers")
router.register('quotes', PolicyViewSet, basename="quotes")

urlpatterns = router.urls
