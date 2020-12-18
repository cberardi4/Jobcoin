#!/usr/bin/env python
import uuid
import sys
import threading
import click
import logging
import time
import os
from jobcoin import mixer

logger = logging.getLogger(__name__)

def setup_logging():
    levels = ['DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL', 'FATAL']

    logger.setLevel(logging.INFO)
    # set format of logging
    log_formatter = logging.Formatter('%(asctime)s [%(name)s] %(levelname)s - %(message)s')

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.ERROR)
    console_handler.setFormatter(log_formatter)

    root_logger = logging.getLogger('')
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(console_handler)

    # get path of current directory for log file
    path = os.path.dirname(os.path.abspath(__file__))
    # create FileHandler - sends logging output to a file
    file_handler = logging.FileHandler(path + '/jobcoin.log')
    file_handler.setFormatter(log_formatter)

    # add the file handler to the logger
    logging.getLogger('').addHandler(file_handler)

@click.command()
def main(args=None):
    print('Welcome to the Jobcoin mixer!\n')

    setup_logging()
    while True:
        new_addresses = click.prompt(
            'Please enter a comma-separated list of new, unused Jobcoin '
            'addresses where your mixed Jobcoins will be sent.',
            prompt_suffix='\n[blank to quit] > ',
            default='',
            show_default=False)
        if new_addresses.strip() == '':
            sys.exit(0)
        new_addresses = new_addresses.split(',')
        deposit_address = uuid.uuid4().hex
        click.echo(
            '\nYou may now send Jobcoins to address {deposit_address}. They '
            'will be mixed and sent to your destination addresses.\n'
              .format(deposit_address=deposit_address))
        # if still true by the end of for loop, then addresses are safe to send to Mixer
        # checking for possible sql attempts before sending address to mixer
        is_alphanumeric = True
        for addr in new_addresses:
            is_alphanumeric = addr.isalnum()
            # someone trying to perform sql injection
            if is_alphanumeric == False:
                print("Not a valid address. Please enter an alphanumeric value.")
                break

        if is_alphanumeric == True:
            logger.info("Final destination addresses given by user: {}".format(new_addresses))
            mixer.run(deposit_address, new_addresses)
            print("...Transactions in progress...")
            if len(new_addresses) <= 3:
                time.sleep(35)
            else:
                time.sleep(100)

if __name__ == '__main__':
    sys.exit(main())
