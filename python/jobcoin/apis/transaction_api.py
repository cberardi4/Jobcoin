import requests
from . import config
from jobcoin.apis.address_api import Address_API

class Transaction_API:

    def __init__(self):
        self.address_api = Address_API()

    def create_transaction(self, from_address, to_address, amount):
        from_address_balance = self.address_api.get_address_balance(from_address)
        # invalid transaction - not enough funds in account
        if amount > from_address_balance:
            print("Invalid Transaction. {} doesn't have enough balance for that transaction.".format(from_address))
            return 'Invalid'

        # invalid transaction - to_address does not exist in Jobcoin
        #if self.address_api.check_activated_address(to_address) == 'unactivated':
        #    print("Invalid Transaction. {} does not exist in Jobcoin.".format(to_address))
        #    return 'Invalid'

        # valid transaction
        else:
            values = self.set_transaction_values(from_address, to_address, amount)
            response = requests.post(config.API_TRANSACTIONS_URL, values)
            return response

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
        # SANITIZE INPUT
        # self.sanitize_input
        return {'fromAddress': from_address, 'toAddress': to_address, 'amount': amount}

    def sanitize_input(self):
        # sanitize input values for value dict to make sure no one is trying to do a sql injection
        print('sanitize_input - transaction')
