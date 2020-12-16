class Transaction:
    '''
    Object that carries all information need from initial transaction (from Source address) through Mixer's algorithm,
    and then distributed into the final destination addresses given by user.
    Class variables:
        - to_address (string): address where current transaction is sending Jobcoin to
        - from_address (string): address where current transaction is sending Jobcoin from
        - amount (float): total Jobcoin getting sent in Mixing algorithm (gets split up during transaction from House address
          to final destination addresses)
        - final_dst_addresses (list): Addresses that User wants the money to be sent to in the very end. Kept this is as a
          list of addresses instead of a flag which indicates which step in the process the Mixer was at. Did not want
          someone with source code to be able to reverse engineer Mixing algorithm.
    '''

    def __init__(self, to_address, from_address, amount, final_dst_addresses):
        '''
        Instantiate Transaction object with all of relevant information.
        '''
        self.to_address = to_address
        self.from_address = from_address
        self.amount = amount
        self.final_dst_addresses = final_dst_addresses

    def get_to_address(self):
        '''
        Return destination address in transaction.
        Return value (string)
        '''
        return self.to_address

    def get_from_address(self):
        '''
        Return source address in transaction.
        Return value (string)
        '''
        return self.from_address

    def get_amount(self):
        '''
        Return amount of Jobcoin being transferred in transaction.
        Return value (float)
        '''
        return self.amount

    def get_final_dst_addresses(self):
        '''
        Return User's final destination addresses in transaction.
        Return value (tuple)
        '''
        return self.final_dst_addresses
