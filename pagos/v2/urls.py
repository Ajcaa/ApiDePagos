from . import api
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'services', api.ServicesViewSet, 'services')
router.register(r'payment', api.PaymentUserViewSet, 'payment')
router.register(r'expired', api.ExpiredPaymentsViewSet, 'expired')

urlpatterns = router.urls