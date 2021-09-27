class MemberNotFound(Exception):
    """Custom Exception for an invalid member id"""
    def __init__(self, member_id):
        self.member_id = member_id

    def __str__(self):
        return "Member ID {} is not found in readings json.".format(self.member_id)


class ReadingNotFound(Exception):
    """Custom Exception for an invalid reading bill date"""
    def __init__(self, bill_date):
        self.bill_date = bill_date

    def __str__(self):
        return "Bill date {} has no reading found for the month in readings json.".format(self.bill_date)


class AccountNotFound(Exception):
    """Custom Exception for an invalid account id of a member"""
    def __init__(self, account_id, member_id):
        self.account_id = account_id
        self.member_id = member_id

    def __str__(self):
        return "AccountID {} not found for member {} in readings json.".format(self.account_id, self.member_id)


class EnergyTypeNotSupported(Exception):
    """Custom Exception for an invalid energy type in readings json"""
    def __init__(self, energy_type):
        self.energy_type = energy_type

    def __str__(self):
        return "Energy type {} is not supported.".format(self.energy_type)


class ReadingUnitNotSupported(Exception):
    """Custom Exception for an invalid reading unit in readings json"""
    def __init__(self, unit):
        self.unit = unit

    def __str__(self):
        return "Energy Unit {} is not supported.".format(self.unit)
