from rest_framework import serializers

from .models import CustomerUser


class CustomerUserSerializer(serializers.ModelSerializer):
    age = serializers.IntegerField(max_value=122, min_value=1)

    class Meta:
        model = CustomerUser
        fields = ('id','name', 'email', 'age',)
