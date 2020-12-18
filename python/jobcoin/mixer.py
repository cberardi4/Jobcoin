import requests
import threading
import time
import queue
import logging
from random import random
from random import seed
from random import randint
from .classes.transaction import Transaction
from .classes.address_api import Address_API
from .classes.transaction_api import Transaction_API

logger = logging.getLogger(__name__)

# new transactions from Source Address --> Deposit Address get placed in here
transaction_queue_deposit = queue.Queue()
# transactions from Deposit Address --> House Address get placed in here
transaction_queue_house = queue.Queue()
HOUSE_ADDRESS = 'House_Address'

'''
Mixer file contains all functions within the Mixing algorithm. The file is called from the cli.py file when it calls the mixer.run()function.
It retrieves transaction details, sanitizes input, and watches for new transactions at the deposit address and house address.
When mixer does notice a transaction at either of the addresses, it proceeds to the next step in the process. Eventually, the total amount is
added into the User's list of final destination addresses, in different transactions, with time spaced in between each incremental transaction.
'''

def initialize_threads(transaction_src_deposit, transaction_api, address_api):
    '''
    This function sets off two threads that are running in the background.
    thread_watching_deposit_addr: This is watching for transactions from the original Source Address --> Deposit Address. When
    a Transaction object is placed in the transaction_queue_deposit queue, the transaction from Deposit Address --> House Address is kicked off.
    thread_watching_house_addr: This is watching for transactions from the Deposit Address --> House Address. When a Transaction object is
    placed in the transaction_queue_house queue, the transaction from House Address --> each individual Destination Address is kicked off.
    '''

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
    '''
    This function asks the User how many Jobcoins they want to transfer in the transaction. It converts input to float and if a non-numeric
    is entered, it continues to ask for the amount until a valid entry is given.
    '''
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
                logger.info("Total transaction amount: {}".format(amount))
                return amount
        # user entered a value that was not a number
        except:
            print("Not a valid input value. Please enter a number.")

def ask_from_address(address_api):
    '''
    This function asks the User what address they want the Jobcoins to come from. If a non-alphanumeric value is entered, it continues
    to ask for the amount until a valid entry is given. This covers for sql injection attemps, which include non-alphanumeric values in
    those attempts. It also makes sure that the source address of the transaction is valid and exists.
    '''
    # Addresses have no real limitations on what characters/length they can be
    # if there was a database connected to users, would check for SQL injection attack substrings (ex: '1=1)
    while True:
        try:
            from_address = input("What address will the transaction come from? ")

            # check for funny business (includes sql injections)
            is_alphanumeric = from_address.isalnum()
            if is_alphanumeric == False:
                print("Not a valid address. Please enter an alphanumeric value.")
                continue

            # make sure the from_address exists --> otherwise, the Jobcoin wouldn't have anywhere to come from
            status = address_api.check_activated_address(from_address)
            if status == 'activated':
                logger.info("Source address given: {}".format(from_address))
                return from_address
            else: # status = unactivated
                print("Source address does not exist. Please enter a valid source address.")
        except:
            print("Not a valid input value. Please enter an address (alphanumeric).")

# Write your Jobcoin API client here.
def run(deposit_address, dst_addresses):
    '''
    This function starts off the entire mixing process. It creates API and Transaction objects for the original transaction from Source --> Deposit.
    It sets off the other threads polling the Jobcoin network, and validates the original transaction was successful.
    '''
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
        logger.info("Transaction between {0} and {1} successful! ".format(from_address, deposit_address))


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
           # create new transaction from deposit address --> house address
           transaction_result = transaction_api.create_transaction(transaction_deposit_house)
           # check that transaction was successful
           if transaction_result != 'Invalid':
               q_len_old = q_len_new
               # add transaction to house address queue
               transaction_queue_house.put(transaction_deposit_house)
               logger.info("Transaction between {0} and {1} successful! ".format(transaction_old.get_to_address(), HOUSE_ADDRESS))

def scramble_transaction_money(address_list, total_amount):
    '''
    Helper function for watch_network_house_addr(). This function splits the total amount (total_amount) of the transfer into n amount of transactions
    (n = number of addresses provided by User). The algorithm then multiplies a randomly created factor between 0.20-0.87 (factor) by the total amount of
    the transfer (total_amount) and assigned to (transaction_n). That value (transaction_n) is added to the dictionary that maps each transaction amount
    for each address (transactions_dict). After, it (transaction_n) is subtracted from the (total_amount). The for loop continues to multiply the factor
    (factor) by the diminishing (total_amount) n-1 times. We want the last transaction amount to just be the remainder from the previous factor multiplication.

    The function also checks to make sure that all of the transaction amounts add up completely to the original total transaction amount (total_amount_original)
    If for some reason it does not, it finds the difference in the sum of the transaction amounts (missing_amount), and adds it to the very first
    item in the list.

    Return value (list):
        - amount for individual transaction (float)
    '''
    # dictionary that assigns a transaction amount to each address
    transactions_dict = {}
    # save total amount at beginning, because the value will be manipulated in for loop
    # check at the very end that the final transaction amounts all add up to the original amount
    total_amount_original = total_amount
    # want fraction to be below 1, but don't want the factor to be so insignificant that it's almost the same
    # as the entire amount, so limiting it to fractions closer to 0.5
    seed(1)
    factor = random()
    num_addrs = len(address_list)
    # using this variable to make sure there is no loss in the total amount due to decimal multiplication
    checking_total_at_end = 0
    for n in range(0,num_addrs-1):
        transaction_n = factor * total_amount
        # assign transaction amount to address at index n
        transactions_dict[address_list[n]]=transaction_n
        checking_total_at_end += transaction_n
        total_amount = total_amount - transaction_n

    # for the last transaction amount, we just want to do whatever is leftover from the last iterations
    # of the factor multiplying
    transactions_dict[address_list[num_addrs-1]]=total_amount
    checking_total_at_end += total_amount

    if checking_total_at_end != total_amount_original:
        missing_amount = total_amount_original - checking_total_at_end
        # avoid an index out of bounds error
        # should always be first item in list
        index_of_transaction_to_add_to = len(num_addrs) - (len(num_addrs)-1)
        # add missing amount to the transaction amount for transaction at index index_of_transaction_to_add_to so that
        # every single fraction of a Jobcoin is accounted for
        transactions_dict[index_of_transaction_to_add_to] = transactions_dict[index_of_transaction_to_add_to] + missing_amount

    return transactions_dict


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
           # get dictionary that will tell how much to transfer per address
           transactions_dict = scramble_transaction_money(final_dst_addresses, transaction_old.get_amount())
           logger.info("Transaction dictionary: {}".format(transactions_dict))
           # addr = final destination address
           for addr,send_amount in transactions_dict.items():
               # come up with arbitratrary time to wait before sending from house to next final destination address
               # only doing seconds (between 0 and 20) for the sake of testing. In real world mixer, I would wait longer
               time_wait = randint(0, 20.0)
               time.sleep(time_wait)
               # create the new transaction object
               # dst = addr, source = HOUSE_ADDRESS
               transaction_deposit_final = Transaction( addr,
                                                        HOUSE_ADDRESS,
                                                        float(send_amount),
                                                        transaction_old.get_final_dst_addresses())
               # create new transaction from house address --> final destination address
               transaction_result = transaction_api.create_transaction(transaction_deposit_final)
               # check that transaction was successful
               if transaction_result != 'Invalid':
                   q_len_old = q_len_new
                   # add transaction to house address queue
                   logger.info("Transaction between {0} and {1} successful! ".format(HOUSE_ADDRESS, addr))
