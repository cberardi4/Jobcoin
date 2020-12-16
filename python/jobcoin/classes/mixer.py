import time
import requests
from jobcoin.apis.transaction_api import Transaction_API
from jobcoin.apis.address_api import Address_API

class Mixer:

    def __init__(self):
        self.transaction_api = Transaction_API()
        self.address_api = Address_API()
        self.house_account = 'HouseAccount'

    def watch_network(self, deposit_address, amount):
        '''
        Continuously checks if any new Jobcoins have been transferred into the House Account.
        If a transaction has occured, Mixer will send the deposited amount from the Deposit
        Address to the House Address.
        '''

        # check if deposit address is valid
        address_status = self.address_api.check_activated_address(deposit_address)
        if address_status == 'activated':
            old_transaction_list = self.address_api.get_address_transactions(deposit_address)
            #print("OLD: {}".format(deposit_address))
        while True:
            new_transaction_list = self.address_api.get_address_transactions(deposit_address)
            #print("NEW: {}".format(new_transaction_list))

            # deposit address has funds
            #if :
                # A new transaction has occured at the deposit address --> need to transfer to house address
            #    if len(new_transaction_list) > len(old_transaction_list):
            #        # create new transaction from deposit address --> house address
            #        transaction_result = transaction_api.create_transaction(deposit_address, house_address, self.house_account)
                    # check that transaction was successful
                    # if transaction_result == 'Invalid':
                #old_transaction_list = new_transaction_list
                #time.sleep(0.1)
