# Overview
There are 4 main coding files added for the problem solution and `tests` folder is added for writing tests.

`member.py` - defines each member with their readings and get energy bills for all accounts from `member_account`.

`member_account.py` - defines members accounts, and their bill calculation for different energy types.

`energy_reading.py` - defines representation of a reading object of an energy type.

`custom_exception.py` - defines custom exceptions for different cases like MemberNotFound, ReadingNotFound, AccountNotFound etc.

`tests` - folder containing tests for all files except `custom_exception`.

# Development

Prerequisites 
* python 3

## SetUp
Create a virtual environment and use it for development and testing purpose. 

You can create virtualenv using below command 
```
virtualenv -p python3 venv
```
**Note:** - Make sure you have virtualenv installed in your system.

Please install the requirements from below files.
* `requirements.txt` - libraries required for production code.
* `requirements-dev.txt` - libraries required for development and test purpose.

# Installation
Install the requirements by below commands:-
```
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

# Run

You can run the program by running `main.py` with 3 optional arguments as explained below.

`member_id` - Member ID present in the readings json. 

`account_id` - Account ID of the member id in readings json, if not provided all accounts considered.

`bill_date` - Billing date that we want to compute the bill for. By default, we expect that the billing period is this 
date minus one month.

# Test

I have used pytest for writing tests. All the tests for additional files are inside `tests` folder. 

To run the tests, you can run the below command:-

```
pytest -v
```

# Enhancement

- I created few custom exceptions for corner edge cases like MemberNotFound, AccountNotFound and few more which shows the whole stack trace. This can be extended with extra edge cases if required easily.
  
- I would move the test `test_bill_member.py` inside the `tests` folder to keep all the tests in one place and run it all together.

- We may implement Schematics for the readings dataset and can validate models based on Member, Account and Reading.
