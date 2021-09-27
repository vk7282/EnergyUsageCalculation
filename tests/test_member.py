# inbuilt libs
import datetime
from copy import deepcopy

# 3rd party libs
import pytest

# project libs
from member import Member
from custom_exception import MemberNotFound, AccountNotFound


@pytest.mark.usefixtures('member_reading')
@pytest.mark.usefixtures('full_reading')
class TestMember:
    """Test for Member Class"""

    def test_init_valid_member_id(self):
        """Test to check if Member is initialized with correct MemberID"""
        member = Member('member-123', self.member_reading)
        assert member.member_id == 'member-123'

    def test_init_invalid_member_id(self):
        """Member should throw InvalidMember exception in case of invalid MemberID"""
        with pytest.raises(MemberNotFound):
            Member('member-123', {})

    def test_init_member_accounts(self):
        """Test to check if an account exists in all accounts from readings after initializing"""
        member = Member('member-123', {'member-123': [{'account-abc': []}]})
        assert 'account-abc' in member.accounts

    def test_len_member_accounts(self):
        """Test to check if initialized member has correct number of readings for an energy type"""
        member = Member('member-123', self.member_reading)
        readings_len = len(member.accounts['account-abc'].billing_readings['electricity'])
        assert readings_len == 2

    def test_calculate_monthly_energy_bill_for_account(self):
        """Test if monthly energy bill for an account calculated matches the expected output"""
        member = Member('member-123', self.member_reading)
        amount, units = member.calculate_monthly_energy_bill_for_account('account-abc', datetime.datetime(2017, 3, 15, 0, 0))
        assert amount == 246.59
        assert units == 2000

    def test_calculate_monthly_energy_bill_for_invalid_account(self):
        """Test if exception is thrown for invalid account id energy bill calculation"""
        member = Member('member-123', self.member_reading)
        with pytest.raises(AccountNotFound):
            member.calculate_monthly_energy_bill_for_account('account-xyz', datetime.datetime(2017, 3, 15, 0, 0))

    def test_calculate_monthly_energy_bill(self):
        """Test if monthly energy bill for all accounts calculated matches the expected output"""
        member = Member('member-123', self.member_reading)
        amount, units = member.calculate_monthly_energy_bill(datetime.datetime(2017, 3, 15, 0, 0))
        assert amount == 246.59
        assert units == 2000

    def test_calculate_monthly_energy_bill_no_accounts(self):
        """Monthly energy bill should be 0 for member with no accounts"""
        member = Member('member-123', {'member-123': []})
        amount, units = member.calculate_monthly_energy_bill(datetime.datetime(2017, 3, 15, 0, 0))
        assert amount == 0
        assert units == 0

    def test_calculate_monthly_energy_bill_with_gas_reading(self):
        """Test if monthly energy bill for all accounts calculated matches the expected output"""
        reading_with_gas = deepcopy(self.member_reading)
        reading_with_gas['member-123'][0]['account-abc'] = self.full_reading
        member = Member('member-123', reading_with_gas)
        amount, units = member.calculate_monthly_energy_bill(datetime.datetime(2017, 3, 15, 0, 0))
        assert amount == 258.01
        assert units == 2100
