import unittest

from bill_member import calculate_bill


class TestBillMember(unittest.TestCase):

    def test_calculate_bill_for_august(self):
        """Bill Calculation for august month should match expected value"""
        amount, kwh = calculate_bill(member_id='member-123',
                                     account_id='ALL',
                                     bill_date='2017-08-31')
        self.assertEqual(amount, 27.57)
        self.assertEqual(kwh, 167)

    def test_calculate_bill_with_invalid_billing_date_format(self):
        """Bill calculation method should throw ValueError in case of wrong format provided for bill date"""
        with self.assertRaises(ValueError):
            calculate_bill(member_id='member-123', account_id='ALL', bill_date='31-08-2017')


if __name__ == '__main__':
    unittest.main()
