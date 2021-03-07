from decimal import Decimal


class Account():
    def __init__(self, number, balance=Decimal(0), total_inflow=Decimal(0), total_outflow=Decimal(0)):
        self.__number = number
        self.__balance = balance
        self.__total_inflow = total_inflow
        self.__total_outflow = total_outflow

    def get_number(self):
        return self.__number

    def get_balance(self):
        return self.__balance

    def get_total_inflow(self):
        return self.__total_inflow

    def set_total_inflow(self, total_inflow):
        self.__total_inflow = self.__total_inflow + total_inflow
        self.__balance = self.__balance + total_inflow

    def get_total_outflow(self):
        return self.__total_outflow

    def set_total_outflow(self, total_outflow):
        self.__total_outflow = self.__total_outflow + total_outflow
        self.__balance = self.__balance + total_outflow
