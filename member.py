# project libs
from member_account import MemberAccount
from custom_exception import AccountNotFound, MemberNotFound


class Member(object):
    """
    A class to represent a Member with ID and readings for energy types
    """

    def __init__(self, member_id, readings):
        """
        Initialize the Member with ID and readings
        :param member_id: Member ID of the member
        :param readings: Readings of the meter for the member id
        """
        self.member_id = member_id
        if self.member_id not in readings:
            raise MemberNotFound(self.member_id)
        self.accounts = self.get_all_accounts_for_member(readings[self.member_id])

    def get_all_accounts_for_member(self, member_readings):
        """
        Process each account of member and stores in a dictionary
        :param member_readings: Member account list with meter readings
        :return: account_dict:  dictionary of accounts with readings for a member
        """
        accounts_dict = {}
        for accounts in member_readings:
            account_id = list(accounts.keys())[0]
            accounts_dict[account_id] = MemberAccount(account_id, accounts[account_id])
        return accounts_dict

    def calculate_monthly_energy_bill_for_account(self, account_id, billing_date):
        """
        Calculate monthly energy bill for given account_id on a billing date
        :param account_id: Account ID of the member
        :param billing_date: Billing date of the month to calculate
        :return: Total amount charged and units consumed
        """
        if account_id not in self.accounts:
            raise AccountNotFound(account_id, self.member_id)
        return self.accounts[account_id].calculate_monthly_bill(billing_date)

    def calculate_monthly_energy_bill(self, billing_date):
        """
        Calculate monthly energy bill for all accounts of a member on a billing date
        :param billing_date: Billing date of the month to calculate
        :return: Total amount charged and units consumed
        """
        total_amount = 0
        total_units = 0
        for account_id in self.accounts:
            amount, units = self.calculate_monthly_energy_bill_for_account(account_id, billing_date)
            total_amount += amount
            total_units += units
        return total_amount, total_units
