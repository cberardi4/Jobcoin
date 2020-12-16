import requests
from . import config

class Address_API:
    '''
    Class that handles all operations/calls from mixer to Jobcoin API regarding addresses.
    All API information comes from config.py file.
    '''

    def check_activated_address(self, address):
        '''
        Checks if address has been activated yet (meaning it has an account with a balance).
        The Jobcoin API states "for an unused address, it will return a balance of 0 and an empty list of transactions."
        Check for this condition.
        Return value (string):
        - 'unactivated' for unactivated accounts
        - 'activated' for already activated accounts
        '''
        transaction_list = self.get_address_transactions(address)
        balance = self.get_address_balance(address)
        # Jobcoin API documentation states "for an unused address, it will return a balance of 0 and an empty list of transactions."
        # check if this condition is true
        if len(transaction_list) == 0 and balance == 0:
            return 'unactivated'
        else:
            return 'activated'


    def get_address_info(self, address):
        '''
        Uses Address_API to get the balance and all transactions for a given address (address).
        Return value (dictionary):
            - account balance (float)
            - list of transactions (list)
        '''
        return requests.get(config.API_ADDRESS_URL+'/{}'.format(address))

    def get_address_transactions(self, address):
        '''
        Uses Address_API to check if there have been any transactions for the given address (address).
        Return value (list):
        - list of past transactions
        '''
        return self.get_address_info(address).json()['transactions']

    def get_address_balance(self, address):
        '''
        Uses Address_API to check the balance of a given address (address).
        Return value (float):
        - balance of given address (address)
        '''
        return float(self.get_address_info(address).json()['balance'])
