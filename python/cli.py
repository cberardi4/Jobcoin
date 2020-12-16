#!/usr/bin/env python
import uuid
import sys

import click

from jobcoin import jobcoin_client


@click.command()
def main(args=None):
    print('Welcome to the Jobcoin mixer!\n')
    while True:
        new_addresses = click.prompt(
            'Please enter a comma-separated list of new, unused Jobcoin '
            'addresses where your mixed Jobcoins will be sent.',
            prompt_suffix='\n[blank to quit] > ',
            default='',
            show_default=False)
        if new_addresses.strip() == '':
            sys.exit(0)
        deposit_address = uuid.uuid4().hex
        click.echo(
            '\nYou may now send Jobcoins to address {deposit_address}. They '
            'will be mixed and sent to your destination addresses.\n'
              .format(deposit_address=deposit_address))

        jobcoin_client.run_mixer(deposit_address, new_addresses)



if __name__ == '__main__':
    sys.exit(main())
