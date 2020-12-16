import requests
from . import config

class Address_API:

    def __init__(self):
      self.address = ''


    def check_activated_address(self, address):
        '''
        Checks if address has been activated yet (meaning it has an account with a balance).
        The Jobcoin API defines an "Unused" address as one with an empty list for the transaction
        variable and a balance of zero.
        Return value (string):
        - 'unactivated' for unactivated accounts
        - 'activated' for already activated accounts
        '''
        transaction_list = self.get_address_transactions(address)
        balance = self.get_address_balance(address)
        #print(address_to_check.json())
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
        - value of given address (address)
        '''
        return float(self.get_address_info(address).json()['balance'])

    def sanitize_input(self):
        print("sanitize_input - address")
