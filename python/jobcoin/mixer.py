import requests
import threading
import time
import queue
import random
from jobcoin.classes.transaction import Transaction
from jobcoin.classes.address_api import Address_API
from jobcoin.classes.transaction_api import Transaction_API

transaction_queue_deposit = queue.Queue()
transaction_queue_house = queue.Queue()
HOUSE_ADDRESS = 'House_Address'

'''
Mixer file contains all functions within the Mixing algorithm. The file is called from the cli.py file calls the run() function.
It retrieves transaction details, sanitizes input, and watches for new transactions at the depost address and house address.
When mixer does notice a transaction, it proceeds to the next step in the process.
'''

def initialize_threads(transaction_src_deposit, transaction_api, address_api):

    # first thread is just watching to see if any Jobcoins have been dropped at deposit address
    thread_watching_deposit_addr = threading.Thread(target=watch_network_deposit_addr,
                                                   args=[transaction_src_deposit, transaction_api, address_api])
    # do not want the thread living after the main thread dies
    thread_watching_deposit_addr.setDaemon(True)
    thread_watching_deposit_addr.start()

    # second thread is periodically sending Jobcoins from house address to final destination addresses
    thread_watching_house_addr = threading.Thread(target=watch_network_house_addr,
                                                   args=[transaction_src_deposit, transaction_api, address_api])
    # do not want the thread living after the main thread dies
    thread_watching_house_addr.setDaemon(True)
    thread_watching_house_addr.start()

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
            else: # status = unactivated
                print("Source address does not exist. Please enter a valid source address.")
        except:
            print("Not a valid input value. Please enter an address (alphanumeric).")

def check_sql_injection():
    print("implement me")

# Write your Jobcoin API client here.
def run(deposit_address, dst_addresses):
    address_api = Address_API()
    transaction_api = Transaction_API()

    # Get necessary transaction details and sanitize input
    amount = ask_amount()
    from_address = ask_from_address(address_api)

    # create Transaction object to store all of transaction information
    transaction_src_deposit = Transaction(deposit_address, from_address, amount, dst_addresses)

    # have Mixer listening for transactions on separate thread immediately
    initialize_threads(transaction_src_deposit, transaction_api, address_api)

    # initial transfer: Source Address --> Mixer's Deposit Address
    response = transaction_api.create_transaction(transaction_src_deposit)
    if response != "Invalid":
        # add transaction to queue for monitoring Mixer
        transaction_queue_deposit.put(transaction_src_deposit)


def watch_network_deposit_addr(transaction_src_deposit, transaction_api, address_api):
    '''
    Continuously checks if any new Jobcoins have been added to the deposit transaction queue.
    If a transaction has occured, Mixer will send the deposited amount from the Deposit
    Address to the House Address.
    '''

    q_len_old = transaction_queue_deposit.qsize()
    while True:
       q_len_new = transaction_queue_deposit.qsize()
       # if the queue size has grown, a transaction has been occured (src address --> deposit address)
       if q_len_old < q_len_new:
           # need to send Jobcoins placed at deposit address into house address
           # first get transaction details for Transaction object from queue
           transaction_old = transaction_queue_deposit.get()
           # create the new transaction object
           # use the get_to_address function because the destination of the first transaction is the source of this transaction
           transaction_deposit_house = Transaction( HOUSE_ADDRESS,
                                                    transaction_old.get_to_address(),
                                                    transaction_old.get_amount(),
                                                    transaction_old.get_final_dst_addresses())
           print("i still know final addresses! {}".format(transaction_old.get_final_dst_addresses()))
           # create new transaction from deposit address --> house address
           transaction_result = transaction_api.create_transaction(transaction_deposit_house)
           # check that transaction was successful
           if transaction_result != 'Invalid':
               q_len_old = q_len_new
               # add transaction to house address queue
               transaction_queue_house.put(transaction_deposit_house)


def watch_network_house_addr(transaction_src_deposit, transaction_api, address_api):
    '''
    Continuously checks if any new Jobcoins have been added to the house transaction queue.
    If a transaction has occured, Mixer will send the deposited amount from the House
    Address to the list of final addresses from User.
    '''

    q_len_old = transaction_queue_house.qsize()
    while True:
       q_len_new = transaction_queue_house.qsize()
       # if the queue size has grown, a transaction has been occured (deposit address --> house address)
       if q_len_old < q_len_new:
           # need to send Jobcoins placed at house address into separate final destination address
           # first get transaction details for Transaction object from queue
           transaction_old = transaction_queue_house.get()
           final_dst_addresses = transaction_old.get_final_dst_addresses()
           print("Final dst addresses: {}".format(final_dst_addresses))
           # split up money between transactions (splitting evenly between addresses)
           send_amount = transaction_old.get_amount()/len(final_dst_addresses)
           # addr = final destination address
           for addr in final_dst_addresses:
               # come up with arbitratrary time to wait before sending from house to next final destination address
               # only doing seconds (between 0 and 20) for the sake of testing. In real world mixer, I would wait longer
               time_wait = random.randint(0, 20.0)
               time.sleep(time_wait)
               # create the new transaction object
               # dst = addr, source = HOUSE_ADDRESS
               transaction_deposit_final = Transaction( addr,
                                                        HOUSE_ADDRESS,
                                                        send_amount,
                                                        transaction_old.get_final_dst_addresses())
               # create new transaction from house address --> final destination address
               transaction_result = transaction_api.create_transaction(transaction_deposit_final)
               # check that transaction was successful
               if transaction_result != 'Invalid':
                   q_len_old = q_len_new
                   # add transaction to house address queue
                   print("Transaction between "+ HOUSE_ADDRESS+" and "+addr+" just occured! ")
