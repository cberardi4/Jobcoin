import requests
import threading
import time
import queue
from jobcoin.classes.mixer import Mixer
from jobcoin.classes.transaction import Transaction
from jobcoin.classes.address_api import Address_API
from jobcoin.classes.transaction_api import Transaction_API

transaction_queue = queue.Queue()

def initialize_polling_threads():
    thread_polling_jobcoin_ntwk = threading.Thread(target=watch_network, args=[])
    # do not want the thread living after the main thread dies
    thread_polling_jobcoin_ntwk.setDaemon(True)
    thread_polling_jobcoin_ntwk.start()


def ask_amount():
    # Get necessary transaction details
    # Sanitize inputs
    while True:
        try:
            amount = float(input("How many Jobcoins would you like to transfer? "))
            # make sure the user is entering a positive number
            if amount <= 0:
                print("Not a valid transfer amount. Value must be greater than zero.")
                # try again
                continue
            # if value is a numeric value over zero, exit While loop ==> valid amount
            else:
                return amount
        # user entered a value that was not a number
        except:
            print("Not a valid input value. Please enter a number.")

def ask_from_address(address_api):
    # Addresses have no real limitations on what characters/length they can be
    # if there was a database connected to users, would check for SQL injection attack substrings (ex: '1=1)
    while True:
        try:
            from_address = input("What address will the transaction come from? ")

            # make sure the from_address exists --> otherwise, the Jobcoin wouldn't have anywhere to come from
            status = address_api.check_activated_address(from_address)
            if status == 'activated':
                return from_address
            else:
                print("Source address does not exist. Please enter a valid source address.")
        except:
            print("Not a valid input value. Please enter an address (alphanumeric).")



# Write your Jobcoin API client here.
def run_mixer(deposit_address, new_addresses):
    address_api = Address_API()
    transaction_api = Transaction_API()
    mixer = Mixer()

    # Get necessary transaction details and sanitize input
    amount = ask_amount()
    from_address = ask_from_address(address_api)

    # create Transaction object to store all of transaction information
    transaction_src_deposit = Transaction(deposit_address, from_address, amount)
    print(transaction_src_deposit.get_from_address())
    # have Mixer listening for transactions on separate thread immediately
    #initialize_polling_threads(transaction_queue)

    # initial transfer: Source Address --> Mixer's Deposit Address
    response = transaction_api.create_transaction(transaction_src_deposit)
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
