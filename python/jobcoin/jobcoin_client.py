import requests
import threading
import time
import queue
from jobcoin.classes.mixer import Mixer
from jobcoin.classes.transaction import Transaction
from jobcoin.apis.address_api import Address_API
from jobcoin.apis.transaction_api import Transaction_API



def initialize_polling_threads(mixer, transaction_src_deposit, transaction_queue):
    thread_polling_jobcoin_ntwk = threading.Thread(target=mixer.watch_network, args=[transaction_src_deposit, transaction_queue])
    # do not want the thread living after the main thread dies
    thread_polling_jobcoin_ntwk.setDaemon(True)
    thread_polling_jobcoin_ntwk.start()

# Write your Jobcoin API client here.
def run_mixer(deposit_address, new_addresses):

    transaction_queue = Queue()

    address_api = Address_API()
    transaction_api = Transaction_API()
    mixer = Mixer()

    # Get necessary transaction details
    amount = float(input("How many Jobcoins would you like to transfer? "))
    from_address = input("What address will the transaction come from? ")

    # sanitize amount
    # sanitize address

    # create Transaction object to store all of transaction information
    transaction_src_deposit = Transaction(deposit_address, from_address, amount)

    # have Mixer listening for transactions on separate thread immediately
    initialize_polling_threads(mixer, transaction_src_deposit, transaction_queue)

    # initial transfer: Source Address --> Mixer's Deposit Address
    response = transaction_api.create_transaction(from_address, deposit_address, amount)
    if response != "Invalid":
        print(response.json())

    # transfer of Deposit Address --> House Account happens in thread_polling_jobcoin_ntwk (mixer) thread


def watch_network(self, transaction_obj):
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
