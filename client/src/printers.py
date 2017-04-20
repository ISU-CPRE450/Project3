def print_title(title):
    title = ' %s ' % title
    print ''
    print '=' * 10 + title + '=' * 10
    print ''


def print_balances(balances):
    print_title('BALANCES')
    for balance in balances:
        print '$' + balance


def print_transactions(user, transactions):
    print_title("TRANSACTION HISTORY")
    for transaction in transactions:
        amount = transaction['fee_paid']
        account_id = transaction['source_account']
        message = 'Received $%s from %s' % (amount, account_id)
        if account_id == user.account_id:
            message = 'Paid $%s' % (amount)
        print message
