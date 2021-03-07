from rest_framework import serializers

from transactions_overview_api.users.models import CustomerUser

from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    reference = serializers.CharField()
    user_id = serializers.IntegerField(write_only=True, min_value=1)

    class Meta:
        model = Transaction
        fields = ('reference', 'date', 'amount', 'type', 'category', 'account', 'user_id',)

    def validate(self, data):
        reference_errors = self.custom_reference_validation(data.get('reference'))
        user_errors = self.custom_user_id_validation(data.get('user_id'))
        amount_errors = self.custom_amount_based_on_type_validation(data.get('type'), data.get('amount'))

        if reference_errors or user_errors or amount_errors:
            errors_list = []
            if reference_errors:
                errors_list.append(reference_errors)
            if user_errors:
                errors_list.append(user_errors)
            if amount_errors:
                errors_list.append(amount_errors)

            errors = {}
            errors[data.get('reference')] = errors_list
            if errors:
                if len(errors_list) == 1:
                    errors[data.get('reference')] = errors_list[0]
                raise serializers.ValidationError(errors)

        super().validate(data)
        return data

    def create(self, validated_data):
        validated_data['user'] = CustomerUser.objects.get(id=validated_data.pop('user_id'))
        return Transaction.objects.create(**validated_data)

    def custom_user_id_validation(self, user_id):
        if not CustomerUser.objects.filter(id=user_id).exists():
            return {str(user_id): 'User not registered.'}

    def custom_reference_validation(self, reference):
        if Transaction.objects.filter(reference=reference).exists():
            return {str(reference): 'Reference already registered.'}

    def custom_amount_based_on_type_validation(self, transaction_type, transaction_amount):
        if transaction_type == 'inflow' and transaction_amount < 0:
            return {str(transaction_amount): 'Amount should be positive for inflow operations.'}
        elif transaction_type == 'outflow' and transaction_amount > 0:
            return {str(transaction_amount): 'Amount should be negative for outflow operations.'}
