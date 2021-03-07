from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'transactions', views.TransactionModelViewSet)
router.register(r'summary-accounts', views.SummaryByAccountViewSet)
router.register(r'summary-categories', views.SummaryByCategoryViewSet)
router.register(r'force-bulk-transactions', views.TransactionForceBulkViewSet)
