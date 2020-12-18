import pytest
from jobcoin.classes.transaction_api import Transaction_API
from jobcoin.classes.address_api import Address_API
from jobcoin.classes.transaction import Transaction

def test_check_activated_address_invalid():
    '''
    Test to make sure that the API does not return a known unactivated address
    as valid/activated.
    '''
    a_api = Address_API()
    result = a_api.check_activated_address('randomaddress')
    assert 'unactivated' == result

def test_check_activated_address_valid():
    '''
    Test to make sure that a known activated address is returned as valid.
    '''
    a_api = Address_API()
    result = a_api.check_activated_address('Tina')
    assert 'activated' == result

def test_address_info():
    '''
    Test to make sure that a dictionary of an account's balance and transactions is returned
    '''
    a_api = Address_API()
    result = a_api.get_address_info('Tina')
    assert 'balance' and 'transactions' in result.json().keys()
