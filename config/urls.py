from django.contrib import admin
from django.urls import include, path, re_path
# from rest_framework_simplejwt import views as jwt_views

from transactions_overview_api.users.routers import router as users_router
from transactions_overview_api.transactions.routers import router as transactions_router

from .schema import schema_view


urlpatterns = [
    re_path(r'^$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('admin/', admin.site.urls),

    path('', include(users_router.urls)),
    path('', include(transactions_router.urls)),
]
