class Transaction:

    def __init__(self, to_address, from_address, amount):
        self.to_address = to_address
        self.from_address = from_address
        self.amount = amount

    def get_to_address(self):
        return self.to_address

    def get_from_address(self):
        return self.from_address

    def get_amount(self):
        return self.amount
