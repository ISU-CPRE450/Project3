from datetime import datetime
import requests

from stellar_base.address import Address
from stellar_base.builder import Builder

SERVER_URL = "http://localhost:9088"


class User(object):

    def __init__(
            self, email=None, account_id=None, password=None, secret=None):
        self.email = email
        self.account_id = account_id
        self.secret = secret
        self.password = password
        self.game_id = None

    def get_game(self):
        if not self.game_id:
            raise Exception("You have not joined a game yet")

    def get_address(self):
        address = Address(address=self.account_id)
        address.get()
        return address

    def get_balance(self):
        balances = self.get_address().balances
        amounts = []
        for balance in balances:
            amounts.append(balance['balance'])
        return amounts

    def get_transactions(self):
        transactions = self.get_address().transactions()
        transactions = transactions['_embedded']['records']
        return self._filter_transactions_within_24_hrs(transactions)

    def _filter_transactions_within_24_hrs(self, transactions):
        now = datetime.utcnow()
        filtered = []
        error = False
        for transaction in transactions:
            try:
                timestamp_str = transaction['created_at']
                timestamp = datetime.strptime(
                    timestamp_str, "%Y-%m-%dT%H:%M:%SZ")
                delta = now - timestamp
                if delta.days > 0:
                    continue
                filtered.append(transaction)
            except:
                error = True
                filtered.append(transaction)

        if error:
            print 'Error filtering transactions to within a day. '\
                  'This report may not be accurate'
        return filtered

    def make_transaction(self, transaction):
        builder = Builder(secret=self.secret)
        builder.append_payment_op(
            transaction.target_account_id, transaction.amount, 'XLM')
        builder.sign()
        builder.submit()


class Banker(User):

    def proctor_new_game(self):
        url = '%s/api/game/%s/' % (SERVER_URL, self.account_id)
        r = requests.post(url)
        if not r.ok:
            raise Exception(r.text)
        data = r.json()
        self.game_id = data['id']

    def disconnect_from_game(self):
        url = '%s/api/game/%s/' % (SERVER_URL, self.game_id)
        self.game_id = None
        r = requests.delete(url)
        if not r.ok:
            raise Exception(r.text)

    def get_participants(self):
        url = '%s/api/game/%s/' % (SERVER_URL, self.game_id)
        r = requests.get(url)
        if not r.ok:
            raise Exception(r.text)
        data = r.json()
        return data['participants']
