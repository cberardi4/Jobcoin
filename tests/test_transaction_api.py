#!/usr/bin/env python
import pytest
from jobcoin.classes.transaction_api import Transaction_API
from jobcoin.classes.address_api import Address_API
from jobcoin.classes.transaction import Transaction

@pytest.fixture
def set_up(to_address, from_address, amount):
    '''
    Create all objects and variables necessary to use the APIs
    '''
    # add 3.5 coins to Tina's account via API
    # come up with dummy values for transaction object
    to_addresses = ['111','222','333']

    transaction_obj = Transaction(to_address, from_address, amount, to_addresses)
    address_api = Address_API()
    transaction_api = Transaction_API()

    return transaction_obj, address_api, transaction_api

def test_create_transaction_valid():
    '''
    Test to make sure that valid transaction details result in a successful transaction via the API.
    '''

    transaction_obj, address_api, transaction_api = set_up('Tina', 'Berardi', .5)
    transaction_result = transaction_api.create_transaction(transaction_obj)

    assert 'Valid' in transaction_result

def test_create_transaction_invalid():
    '''
    Test to make sure that transaction fails because trying to withdraw more money than source
    account has in it.
    '''
    # check balance of source account so we can make transfer amount larger than that
    address_api = Address_API()
    balance = address_api.get_address_balance("Tina")
    amount = balance + 2.0

    # attempt invalid transaction
    transaction_obj, address_api, transaction_api = set_up('Tina','Berardi', amount)
    transaction_result = transaction_api.create_transaction(transaction_obj)

    assert 'Invalid' in transaction_result

def test_get_all_transactions():
    '''
    Test that get_all_transactions returns a large list.
    '''
    transaction_obj, address_api, transaction_api = set_up('Tina', 'Berardi', 1.0)
    list_transactions = transaction_api.get_all_transactions()
    assert list_transactions.status_code is 200

def test_set_transaction_values():
    '''
    Make sure that transaction values in dict match your input values
    '''
    transaction_obj, address_api, transaction_api = set_up('Tina', 'Berardi', 1.0)
    transaction_api.set_transaction_values('Tina', 'Berardi', 1.0)
