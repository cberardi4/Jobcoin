class Transaction:

    def __init__(self, to_address, from_address, amount, final_dst_addresses):
        self.to_address = to_address
        self.from_address = from_address
        self.amount = amount
        self.final_dst_addresses = final_dst_addresses

    def get_to_address(self):
        return self.to_address

    def get_from_address(self):
        return self.from_address

    def get_amount(self):
        return self.amount

    def get_final_dst_addresses(self):
        return self.final_dst_addresses
