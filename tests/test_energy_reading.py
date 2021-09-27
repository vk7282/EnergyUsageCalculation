# inbuilt libs
import datetime
from copy import deepcopy

# 3rd party libs
import pytest

# project libs
from energy_reading import EnergyReading
from custom_exception import ReadingUnitNotSupported


@pytest.mark.usefixtures("energy_reading")
class TestReading:
    """Test for EnergyReading Class"""

    def test_init_reading_date(self):
        """Test to check if EnergyReading is initialized with correct datetime"""
        reading = EnergyReading(self.energy_reading)
        assert reading.reading_date == datetime.datetime(2017, 3, 28, 0, 0)

    def test_init_cumulative(self):
        """Test to check if EnergyReading is initialized with correct cumulative value"""
        reading = EnergyReading(self.energy_reading)
        assert reading.cumulative == 17580

    def test_init_unit(self):
        """Test to check if EnergyReading is initialized with correct unit"""
        reading = EnergyReading(self.energy_reading)
        assert reading.unit == 'kWh'

    def test_init_invalid_unit(self):
        """EnergyReading should throw InvalidReadingUnit exception in case of wrong unit"""
        invalid_unit_reading = deepcopy(self.energy_reading)
        invalid_unit_reading['unit'] = "w"
        with pytest.raises(ReadingUnitNotSupported):
            EnergyReading(invalid_unit_reading)
