#!/usr/bin/env python
import uuid
import sys
import threading
import click

from jobcoin import mixer


@click.command()
def main(args=None):
    print('Welcome to the Jobcoin mixer!\n')

    # what holds each transaction from src --> deposit. For the Mixer to watch if a transaction has occured

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
        mixer.run(deposit_address, new_addresses)


if __name__ == '__main__':
    sys.exit(main())
