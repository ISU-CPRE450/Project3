from datetime import datetime
import hashlib
import json
import random
import requests
import sys

from stellar_base.address import Address
from stellar_base.builder import Builder

from src import printers
from src.transaction import Transaction

SERVER_URL = "http://localhost:9088"


class User(object):

    def __init__(
            self, email=None, account_id=None, password=None, secret=None):
        self.email = email
        self.account_id = account_id
        self.secret = secret
        self.password = password
        self.game_id = None
        self.random_value = None

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

    def get_winner(self):
        url = '%s/api/game/%s/' % (SERVER_URL, self.game_id)
        r = requests.get(url)
        if not r.ok:
            raise Exception(r.text)
        data = r.json()
        p1 = data['participants'][0]
        p2 = data['participants'][1]
        self._validate_random_values(p1, p2)
        value = (p1['random_value'] + p2['random_value']) % 2
        if value > 0:
            return p2
        return p1

    def _validate_random_values(self, p1, p2):
        if p1['hash_value'] != hashlib.sha224(
                str(p1['random_value'])).hexdigest():
            raise Exception('Hash value invalid. Canceling game.')
        elif p2['hash_value'] != hashlib.sha224(
                str(p2['random_value'])).hexdigest():
            raise Exception('Hash value invalid. Canceling game.')

    def get_and_print_latest_game_transactions(self):
        url = '%s/api/game/history/' % (SERVER_URL)
        r = requests.get(url)
        if not r.ok:
            raise Exception(r.text)
        data = r.json()
        printers.print_title('GAME HISTORY (within last 24 hrs)')
        for game in data:
            printers.print_game(game)


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
        print url
        self.game_id = None
        requests.delete(url)

    def get_participants(self):
        url = '%s/api/game/%s/' % (SERVER_URL, self.game_id)
        r = requests.get(url)
        if not r.ok:
            raise Exception(r.text)
        data = r.json()
        return data['participants']

    def give_earnings(self, winner, loser):
        print 'Giving earnings to winner...'
        total_bet = winner['bet_amount'] + loser['bet_amount']
        winner_amount = total_bet * 0.95
        t = Transaction(winner['user']['account_id'], winner_amount)
        self.make_transaction(t)
        print 'Funds have been transferred'

    def resolve_bad_hash(self):
        print 'Transferring funds back into accounts...'
        participants = self.get_participants()
        for p in participants:
            t = Transaction(p['user']['account_id'], p['bet_amount'])
            self.make_transaction(t)
        print 'Funds have been transferred'


class Participant(User):

    def join_game(self, amount):
        url = '%s/api/game/join/%s/' % (SERVER_URL, self.account_id)
        payload = {
            'amount': amount,
            'hash_value': self._compute_hash_value(),
            'random_value': self.random_value
        }
        headers = {'Content-Type': 'application/json'}
        r = requests.post(url, headers=headers, data=json.dumps(payload))
        if not r.ok:
            raise Exception(r.text)
        print 'Game joined!'
        data = r.json()
        self.game_id = data['id']
        t = Transaction(data['banker']['account_id'], amount)
        print 'Transferring funds to bank...'
        self.make_transaction(t)
        print 'Funds have been transferred'

    def get_other_player(self):
        url = '%s/api/game/%s/' % (SERVER_URL, self.game_id)
        r = requests.get(url)
        if not r.ok:
            raise Exception(r.text)
        data = r.json()
        participants = data['participants']
        for p in participants:
            if p['user']['account_id'] != self.account_id:
                return p
        return None

    def get_result(self):
        winner = self.get_winner()
        if winner['user']['account_id'] == self.account_id:
            player = self.get_other_player()
            return 'You won $%s! Funds will be transferred shortly.' % (
                player['bet_amount'])
        return 'You lost. Funds will be transferred shortly.'

    def _compute_hash_value(self):
        self.random_value = random.randint(1, (sys.maxint / 2) - 1)
        return hashlib.sha224(str(self.random_value)).hexdigest()

    def get_and_print_latest_game(self):
        url = '%s/api/game/latest/' % (SERVER_URL)
        r = requests.get(url)
        if not r.ok:
            raise Exception(r.text)
        printers.print_title('MOST RECENT GAME')
        printers.print_game(r.json())
