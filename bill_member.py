# inbuilt libs
import datetime

# project libs
import load_readings
from member import Member


def calculate_bill(member_id=None, account_id=None, bill_date=None):
    """
    Calculate bill of a member id for account on a billing date
    :param member_id: Member ID of a member
    :param account_id: Account ID of the member or ALL
    :param bill_date: Billing date of the month to calculate
    :return: amount: Total amount calculated for a member on the billing date
    :return: kwh: Total units consumed for a member on the billing date
    """
    # we want to throw ValueError in conversion of bill date if proper format for billing date is not provided.
    billing_date = datetime.datetime.strptime(bill_date, "%Y-%m-%d")
    readings = load_readings.get_readings()
    member = Member(member_id, readings)
    if account_id == 'ALL':
        amount, kwh = member.calculate_monthly_energy_bill(billing_date)
    else:
        amount, kwh = member.calculate_monthly_energy_bill_for_account(account_id, billing_date)
    return amount, kwh


def calculate_and_print_bill(member_id, account, bill_date):
    """Calculate the bill and then print it to screen.
    Account is an optional argument - I could bill for one account or many.
    There's no need to refactor this function."""
    member_id = member_id or 'member-123'
    bill_date = bill_date or '2017-08-31'
    account = account or 'ALL'
    amount, kwh = calculate_bill(member_id, account, bill_date)
    print('Hello {member}!'.format(member=member_id))
    print('Your bill for {account} on {date} is £{amount}'.format(
        account=account,
        date=bill_date,
        amount=amount))
    print('based on {kwh}kWh of usage in the last month'.format(kwh=kwh))
