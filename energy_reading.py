import datetime
from custom_exception import ReadingUnitNotSupported


class EnergyReading(object):
    """A class to represent a reading object from an account of a member"""

    UNIT_TYPES = ('kWh',)

    def __init__(self, reading):
        """
        Initialize the reading of an energy type for a member account
        :param reading: Reading of an energy type
        """
        self.reading_date = datetime.datetime.strptime(reading['readingDate'][0:10], "%Y-%m-%d")
        self.cumulative = reading['cumulative']
        if reading['unit'] not in self.UNIT_TYPES:
            raise ReadingUnitNotSupported(reading['unit'])
        self.unit = reading.get('unit')
