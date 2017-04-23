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


def print_game(game):
    print '=' * 40
    print 'Time:', game['time_created']
    p1 = game['participants'][0]
    p2 = game['participants'][1]
    value = (p1['random_value'] + p2['random_value']) % 2
    player_number = 1
    if value > 0:
        player_number = 2
    for i, p in enumerate(game['participants']):
        print 'Player', i + 1, '(%s)' % p['user']['account_id']
        print '\tBet Amount:', p['bet_amount']
        print '\tGuessed Number:', p['random_value']
    print 'Winner: Player', player_number
