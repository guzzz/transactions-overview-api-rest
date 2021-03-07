from decimal import Decimal
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response

from transactions_overview_api.users.models import CustomerUser

from .models import Transaction
from .serializers import TransactionSerializer
from .entities import Account
from .services import *


class TransactionModelViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def create(self, request, *args, **kwargs):
        list_request = isinstance(request.data, list)
        if list_request:
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data, many=False)

        if serializer.is_valid():
            try:
                response_data = transaction_successful_response(self, serializer.save())
                return Response(data=response_data ,status=status.HTTP_201_CREATED)
            except Exception as error:
                error_detail = clean_bulk_errors(None, error)
                return Response(data={
                            "error(s)": "The operation was partial, because some transaction failed.",
                            "transaction": error_detail,
                            "info": "All transactions inserted after this transaction were aborted."
                        },
                        status=status.HTTP_207_MULTI_STATUS
                    )
        else:
            return Response(data={"error(s)": clean_errors(serializer.errors, list_request)}, status=status.HTTP_400_BAD_REQUEST)


class TransactionForceBulkViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def create(self, request, *args, **kwargs):
        list_request = isinstance(request.data, list)
        if list_request:
            transactions_list = request.data
            saved_transactions = []
            error_transactions = []
            for transaction in transactions_list:
                try:
                    custom_validation_error = validate_amount_based_on_type(self, transaction)
                    if custom_validation_error.get('error'):
                        raise Exception('type_and_amount', custom_validation_error.get('detail'))
                    user = CustomerUser.objects.get(id=transaction.get('user_id'))
                    saved_transaction = create_transaction_service(transaction, user)
                    saved_transactions.append(self.serializer_class(saved_transaction).data)
                except Exception as error:
                    error_transactions.append(clean_bulk_errors(transaction.get('reference'), error))
            
            status_code = get_bulk_transactions_status_code(saved_transactions, error_transactions)
            return Response(data={"successful": saved_transactions, "failed": error_transactions}, status=status_code)
        else:
            return Response(data={"error": 'This request only accepts lists.'}, status=status.HTTP_400_BAD_REQUEST)


class SummaryByAccountViewSet(viewsets.ViewSet):
    queryset = CustomerUser.objects.all()

    def retrieve(self, request, pk=None):
        user = CustomerUser.objects.filter(id=pk).first()

        if user:
            start_date, end_date = get_filters(request)
            all_transactions = Transaction.objects.filter(user__id=user.id, date__gte=start_date, date__lte=end_date)
            all_accounts = all_transactions.values_list('account', flat=True).distinct()

            accounts_list = []
            for account in all_accounts:
                account_obj = Account(account)
                account_transactions = all_transactions.filter(account=account)
                for transaction in account_transactions:
                    if transaction.type == 'inflow':
                        account_obj.set_total_inflow(transaction.amount)
                    else:
                        account_obj.set_total_outflow(transaction.amount)
                accounts_list.append(account_obj)
            return Response(data=summary_by_account_response(accounts_list), status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class SummaryByCategoryViewSet(viewsets.ViewSet):
    queryset = CustomerUser.objects.all()

    def retrieve(self, request, pk=None):
        user = CustomerUser.objects.filter(id=pk).first()

        if user:
            inflow = {}
            outflow = {}
            all_transactions = Transaction.objects.filter(user__id=user.id)
            
            for transaction in all_transactions:
                if transaction.type == 'inflow':
                    dict_type = inflow
                else:
                    dict_type = outflow

                if transaction.category in dict_type:
                    current_amount = dict_type.get(transaction.category)
                    new_amount = transaction.amount + Decimal(current_amount)
                    dict_type.update({transaction.category: str(new_amount)})
                else:
                    dict_type.update({transaction.category: str(transaction.amount)})

            return Response(data={"inflow": inflow, "outflow": outflow}, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
