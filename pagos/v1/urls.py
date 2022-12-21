from . import api
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'pagos', api.PagoViewSet, 'pagos')

urlpatterns = router.urls