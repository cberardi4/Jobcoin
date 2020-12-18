import pytest
from jobcoin.classes.transaction import Transaction


def test_get_to_address():
    '''
    Make sure that to_address accessor method works correctly
    '''
    transaction = Transaction('Tina', 'Berardi', 0.2, ['22','33','44'])
    result = transaction.get_to_address()
    assert result == 'Tina'

def test_get_from_address():
    '''
    Make sure that from_address accessor method works correctly
    '''
    transaction = Transaction('Tina', 'Berardi', 0.2, ['22','33','44'])
    result = transaction.get_from_address()
    assert result == 'Berardi'

def test_get_amount():
    '''
    Make sure that amount accessor method works correctly
    '''
    transaction = Transaction('Tina', 'Berardi', 0.2, ['22','33','44'])
    result = transaction.get_amount()
    assert result == 0.2

def test_get_final_addresses():
    '''
    Make sure that final_addresses accessor method works correctly
    '''
    transaction = Transaction('Tina', 'Berardi', .2, ['22','33','44'])
    result = transaction.get_final_dst_addresses()
    assert result == ['22','33','44']
