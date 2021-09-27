# inbuilt libs
from calendar import monthrange

# 3rd party libs
from dateutil.relativedelta import relativedelta

# project libs
from energy_reading import EnergyReading
from tariff import BULB_TARIFF
from custom_exception import ReadingNotFound, EnergyTypeNotSupported


class MemberAccount(object):
    """
    A class to represent a MemberAccount with AccountID and readings for energy types
    """

    BILLING_TYPES = ('electricity', 'gas')

    def __init__(self, account_id, readings):
        """
        Initialize an account of a member with the readings for different energy types
        :param account_id: Account ID of the member
        :param readings: List of meter readings for energy types (electricity, gas)
        """
        self.account_id = account_id
        self.billing_readings = {}
        for meter_readings in readings:
            for billing_type in meter_readings:
                if billing_type not in self.BILLING_TYPES:
                    raise EnergyTypeNotSupported(billing_type)
                self.billing_readings[billing_type] = self.get_readings_for_account(meter_readings[billing_type])

    def get_readings_for_account(self, billing_readings):
        """
        Process each meter reading and append to a billing readings list
        :param billing_readings: list of meter readings of an energy type
        :return: billing_readings_list: Sorted list of billing readings list
        """
        billing_readings_list = []
        for reading in billing_readings:
            billing_readings_list.append(EnergyReading(reading))
        return sorted(billing_readings_list, key=lambda monthly_reading: monthly_reading.reading_date)

    def get_month_reading_for_billing_date(self, billing_type, bill_date):
        """
        Get the reading of the billing date month and year otherwise raise exception
        :param billing_type: Energy type i.e. electricity or gas
        :param bill_date: Billing date of the month to calculate bill
        :return: reading: Reading object if matches billing date else Exception
        """
        readings = self.billing_readings[billing_type]
        for reading in readings:
            if reading.reading_date.year == bill_date.year and reading.reading_date.month == bill_date.month:
                return reading
        else:
            raise ReadingNotFound(bill_date)

    def calculate_monthly_bill_for_billing_type(self, billing_type, billing_date):
        """
        Calculate monthly bill of an account for an energy type on a billing date
        :param billing_type: Energy type i.e electricity or gas
        :param billing_date: Billing date of the month to calculate bill
        :return: total_cost: total cost of an energy type for a billing date
        :return: units_consumed: total units consumed of an energy type for a billing date
        """
        billing_date_reading = self.get_month_reading_for_billing_date(billing_type, billing_date)
        previous_month_billing_date = billing_date - relativedelta(months=1)
        previous_month_reading = self.get_month_reading_for_billing_date(billing_type, previous_month_billing_date)
        units_consumed = billing_date_reading.cumulative - previous_month_reading.cumulative
        num_of_days_in_month = monthrange(billing_date.year, billing_date.month)[1]
        monthly_charge = num_of_days_in_month * BULB_TARIFF[billing_type]['standing_charge']
        units_cost = units_consumed * BULB_TARIFF[billing_type]['unit_rate']
        total_cost = units_cost + monthly_charge
        return total_cost, units_consumed

    def calculate_monthly_bill(self, billing_date):
        """
        Calculate monthly bill of an account of a member on a billing date
        :param billing_date: Billing date of the month to calculate bill
        :return: total_amount: total amount of both energy types for a billing date
        :return: total_units: total units consumed of both energy types for a billing date
        """
        total_amount = 0
        total_units = 0
        for billing_type in self.billing_readings:
            # calculate monthly bill for each energy type if reading exists i.e electricity or gas
            if not self.billing_readings[billing_type]:
                print("No reading found for energy type {}.".format(billing_type))
                continue
            amount, units = self.calculate_monthly_bill_for_billing_type(billing_type, billing_date)
            total_amount += amount
            total_units += units
        return round(total_amount/100, 2), total_units

