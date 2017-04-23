import base64
import getpass
import re

from src.transaction import Transaction
from src.user_factory import LoginFactory, NewAccountFactory


class Prompter(object):
    LOGIN = "login"
    CREATE_ACCT = "create_acct"

    @staticmethod
    def login_or_create_acct():
        while True:
            print "1. Login"
            print "2. Create Account"
            num = raw_input("Enter number: ")
            if num == '1':
                return LoginFactory()
            elif num == '2':
                return NewAccountFactory()
            print "Unrecognized option: '%s'" % num

    @staticmethod
    def request_credentials():
        # TODO remove -- used for faster development
        '''
        if True:
            return {
                'email': 'mcgovern@iastate.edu',
                'password': base64.b64encode('pass')
            }
        '''
        d = {'email': None, 'password': None}
        while True:
            email = raw_input('Enter email: ')
            email_regex_pattern = '[^@]+@[^@]+\.[^@]+'
            if not re.match(email_regex_pattern, email):
                print "Invalid email: %s" % email
                continue
            password = getpass.getpass('Password: ')
            d['email'] = email
            d['password'] = base64.b64encode(password)
            return d

    @staticmethod
    def request_transaction_data():
        account_id = None
        while True:
            if not account_id:
                account_id = raw_input('Enter target account id: ')
            amount_str = raw_input('Enter amount you wish to transfer: $')
            amount = None
            try:
                amount = float(amount_str)
            except:
                print 'Amount must be a float'
                continue
            return Transaction(account_id, amount)

    @staticmethod
    def request_bet_amount():
        while True:
            amount_str = raw_input('Enter amount you wish to bet: $')
            try:
                return float(amount_str)
            except:
                print 'Amount must be a float'
