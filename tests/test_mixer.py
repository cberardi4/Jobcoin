# !/usr/bin/env python
import pytest
import queue
from jobcoin.classes.transaction_api import Transaction_API
from jobcoin.classes.address_api import Address_API
from jobcoin.classes.transaction import Transaction
from jobcoin import mixer

def test_scramble_transaction_money():
    '''
    Test to make sure that the scrambler is transferring the exact amount after splitting
    up Jobcoin into n transactions.
    '''
    address_list = ['22', '33', '44']
    transaction_amount = 3.0

    transaction_dict = mixer.scramble_transaction_money(address_list, transaction_amount)
    sum = 0
    for key,value in transaction_dict.items():
        sum += value

    assert sum == transaction_amount
