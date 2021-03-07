from decimal import Decimal
from datetime import datetime
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from rest_framework import status

from .models import Transaction


def summary_by_account_response(accounts):
    response = []
    for account in accounts:
        response.append({
            "account": account.get_number(),
            "balance": str(account.get_balance()),
            "total_inflow": str(account.get_total_inflow()),
            "total_outflow": str(account.get_total_outflow())
        })
    return response

def get_filters(request):
    if request.query_params.get('start_date', None):
        str_start_date = request.query_params.get('start_date')
    else:
        str_start_date = '1900-01-01'

    if request.query_params.get('end_date', None):
        str_end_date = request.query_params.get('end_date')
    else:
        str_end_date = '2200-01-01'

    start_date = datetime.strptime(str_start_date, "%Y-%m-%d").date()
    end_date = datetime.strptime(str_end_date, "%Y-%m-%d").date()

    return start_date, end_date


def clean_errors(serializer_errors, list_request):
    if list_request:
        return list(filter(None, serializer_errors))
    else:
        return serializer_errors


def clean_bulk_errors(reference, error):
    if type(error) == IntegrityError:
        final_error = error.args[0].split('DETAIL:  ')[1]
        return final_error.split("\n")[0]
    elif type(error) == ValidationError:
        str_error = str(error)
        str_error = str_error[2:-3]
        return f"Key (reference)=({reference}) {str_error}"
    elif error.args[0]=='type_and_amount':
        str_error = str(error.args[1])
        str_error = str_error[1:-1]
        return f"Key (reference)=({reference}) {str_error}"
    else:
        return f"Key (reference)=({reference}) {error.args[0]}"


def transaction_successful_response(self, serializer_saved_return):
    if isinstance(serializer_saved_return, list):
        response = []
        for transaction in serializer_saved_return:
            response.append(self.serializer_class(transaction).data)
        return response
    else:
        return self.serializer_class(serializer_saved_return).data


def validate_amount_based_on_type(self, transaction):
    error = self.serializer_class.custom_amount_based_on_type_validation(
                    self,
                    transaction.get('type'),
                    Decimal(transaction.get('amount'))
                )
    if error:
        validation = dict(error=True, detail=error)
    else:
        validation = dict(error=False)
    return validation


def create_transaction_service(transaction_data, user):
    return Transaction.objects.create(
            reference=transaction_data.get('reference'),
            account=transaction_data.get('account'),
            date=transaction_data.get('date'),
            amount=transaction_data.get('amount'),
            type=transaction_data.get('type'),
            category=transaction_data.get('category'),
            user=user
        )


def get_bulk_transactions_status_code(saved_transactions, error_transactions):
    if not saved_transactions:
        status_code = status.HTTP_400_BAD_REQUEST
    elif not error_transactions:
        status_code = status.HTTP_201_CREATED
    else:
        status_code = status.HTTP_207_MULTI_STATUS
    return status_code
