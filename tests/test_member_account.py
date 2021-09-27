# inbuilt libs
import datetime
from copy import deepcopy

# 3rd party libs
import pytest

# project libs
from member_account import MemberAccount
from energy_reading import EnergyReading
from custom_exception import ReadingNotFound, EnergyTypeNotSupported


@pytest.mark.usefixtures('account_reading')
@pytest.mark.usefixtures('full_reading')
class TestAccount:
    """Test for MemberAccount class"""

    def test_init_account_id(self):
        """Test to check if Member Account is initialized with correct account id"""
        account = MemberAccount('account-abc', self.account_reading)
        assert account.account_id == 'account-abc'

    def test_init_invalid_energy_type(self):
        """MemberAccount should throw an InvalidEnergyType exception for invalid energy type"""
        invalid_energy_type = deepcopy(self.account_reading)
        invalid_energy_type[0]['water'] = []
        with pytest.raises(EnergyTypeNotSupported):
            MemberAccount('account-abc', invalid_energy_type)

    def test_billing_readings_len(self):
        """Test to check if member account has correct number of readings for an energy type"""
        account = MemberAccount('account-abc', self.account_reading)
        assert len(account.billing_readings['electricity']) == 2

    def test_billing_readings_instance_of_energy_reading(self):
        """Test to check if member account has correct reading object"""
        account = MemberAccount('account-abc', self.account_reading)
        assert isinstance(account.billing_readings['electricity'][0], EnergyReading)
        assert isinstance(account.billing_readings['electricity'][1], EnergyReading)

    def test_billing_readings_sorted(self):
        """Test to check if billing readings is sorted and lowest date should appear first"""
        account = MemberAccount('account-abc', self.account_reading)
        assert account.billing_readings['electricity'][0].reading_date == datetime.datetime(2017, 2, 28, 0, 0)

    def test_get_month_reading_for_bill_date(self):
        """Test to check if billing date exists in readings and return that reading object correctly"""
        account = MemberAccount('account-abc', self.account_reading)
        reading = account.get_month_reading_for_billing_date('electricity', datetime.datetime(2017, 3, 15, 0, 0))
        assert reading.reading_date == datetime.datetime(2017, 3, 28, 0, 0)

    def test_get_month_reading_for_bill_date_exception(self):
        """Test to check if non-existing billing date in readings should raise exception"""
        account = MemberAccount('account-abc', self.account_reading)
        with pytest.raises(ReadingNotFound):
            account.get_month_reading_for_billing_date('electricity', datetime.datetime(2020, 3, 15, 0, 0))

    def test_calculate_monthly_bill_for_billing_type(self):
        """
        Test if monthly bill is calculated correctly for electricity and matches the expected output.
        """
        account = MemberAccount('account-abc', self.account_reading)
        total_cost, total_units = account.calculate_monthly_bill_for_billing_type('electricity',
                                                                                  datetime.datetime(2017, 3, 15, 0, 0))
        assert total_cost == 24659.36
        assert total_units == 2000

    def test_calculate_monthly_bill(self):
        """Test if monthly bill is calculated correctly for an account"""
        account = MemberAccount('account-abc', self.account_reading)
        total_cost, total_units = account.calculate_monthly_bill(datetime.datetime(2017, 3, 15, 0, 0))
        assert total_cost == 246.59
        assert total_units == 2000

    def test_calculate_monthly_bill_with_gas_reading(self):
        """Test if monthly bill is calculated correctly for an account with gas readings"""
        account = MemberAccount('account-abc', self.full_reading)
        total_cost, total_units = account.calculate_monthly_bill(datetime.datetime(2017, 3, 15, 0, 0))
        assert total_cost == 258.01
        assert total_units == 2100

    def test_calculate_monthly_bill_no_reading(self):
        """Monthly bill should be 0 if no readings exists for energy types"""
        empty_reading = deepcopy(self.account_reading)
        empty_reading[0]['electricity'] = []
        empty_reading[0]['gas'] = []
        account = MemberAccount('account-abc', empty_reading)
        total_cost, total_units = account.calculate_monthly_bill(datetime.datetime(2017, 3, 15, 0, 0))
        assert total_cost == 0
        assert total_units == 0

