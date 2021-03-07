from rest_framework import viewsets, mixins
from django_filters.rest_framework import DjangoFilterBackend

from .models import CustomerUser
from .serializers import CustomerUserSerializer


class CustomerUserViewSet(mixins.CreateModelMixin, 
                   mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = CustomerUser.objects.all()
    serializer_class = CustomerUserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['email']
