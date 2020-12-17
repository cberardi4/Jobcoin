import requests
import logging
from . import config
from jobcoin.classes.address_api import Address_API
from jobcoin.classes.transaction import Transaction

logger = logging.getLogger(__name__)

class Transaction_API:
    '''
    Class that handles all operations/calls from mixer to Jobcoin API regarding transactions.
    All API information comes from config.py file.
    '''

    def __init__(self):
        '''
        Instantiate Transaction_API object. Need address API for checking if transactions are valid.
        '''
        self.address_api = Address_API()

    def create_transaction(self, transaction):
        '''
        Creates a new Jobcoin transaction.
        Return value (string):
            - "Invalid" for transactions that failed
            - "Valid" if transaction was successful
        '''
        # Get transaction details from transaction object
        from_address = transaction.get_from_address()
        to_address = transaction.get_to_address()
        amount = transaction.get_amount()

        # check source address balance: make sure it's not sending more than it has in the Jobcoin account
        from_address_balance = self.address_api.get_address_balance(from_address)
        # invalid transaction - not enough funds in account
        if amount > float(from_address_balance):
            print("Invalid Transaction. {} doesn't have enough balance for that transaction.".format(from_address))
            return 'Invalid'

        # valid transaction
        else:
            values = self.set_transaction_values(from_address, to_address, amount)
            response = requests.post(config.API_TRANSACTIONS_URL, values)
            return 'Valid'

    def get_all_transactions(self):
        '''
        Lists every Jobcoin transaction.
        Return value (dictionary):
            - balance (string)
            - transactions (list)

        '''
        return requests.get(config.API_TRANSACTIONS_URL)

    def set_transaction_values(self, from_address, to_address, amount):
        '''
        Sets the necessary values to perform a transaction with the Jobcoin API
        Return value (dictionary):
        - from_address (string)
        - to_address (string)
        - amount (sting)
        '''
        return {'fromAddress': from_address, 'toAddress': to_address, 'amount': amount}
