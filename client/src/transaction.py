class Transaction(object):

    def __init__(self, target_account_id, amount):
        self.target_account_id = target_account_id
        self.amount = amount
