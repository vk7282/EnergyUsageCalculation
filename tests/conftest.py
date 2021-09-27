# inbuilt libs
from copy import deepcopy

# 3rd party libs
import pytest


READING = {
    'member-123': [
        {
            'account-abc': [{
                "electricity": [
                    {
                        "cumulative": 17580,
                        "readingDate": "2017-03-28T00:00:00.000Z",
                        "unit": "kWh"
                    },
                    {
                        "cumulative": 15580,
                        "readingDate": "2017-02-28T00:00:00.000Z",
                        "unit": "kWh"
                    }
                ]
            }]
        }
    ]
}

GAS_READING = [
        {
            "cumulative": 5100,
            "readingDate": "2017-03-28T00:00:00.000Z",
            "unit": "kWh"
        },
        {
            "cumulative": 5000,
            "readingDate": "2017-02-28T00:00:00.000Z",
            "unit": "kWh"
        }
    ]


@pytest.fixture(scope='class')
def energy_reading(request):
    energy_reading = READING['member-123'][0]['account-abc'][0]['electricity'][0]
    request.cls.energy_reading = energy_reading


@pytest.fixture
def member_reading(request):
    request.cls.member_reading = READING


@pytest.fixture
def account_reading(request):
    account_reading = READING['member-123'][0]['account-abc']
    request.cls.account_reading = account_reading


@pytest.fixture
def full_reading(request):
    full_reading = deepcopy(READING['member-123'][0]['account-abc'])
    full_reading[0]['gas'] = GAS_READING
    request.cls.full_reading = full_reading

