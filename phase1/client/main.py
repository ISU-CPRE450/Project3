from src.prompter import Prompter
from src import printers
print "=" * 20 + " WELCOME TO COIN FLIPPER APP " + "=" * 20

user = None
while user is None:
    user_factory = Prompter.login_or_create_acct()
    user_factory.print_title()
    creds = Prompter.request_credentials()
    user_factory.email = creds['email']
    user_factory.password = creds['password']
    try:
        user = user_factory.get_or_create_user()
    except Exception as e:
        print "Failure:", e.message

while True:
    printers.print_title(user.email + ' Home Screen')
    print "1. Check Balance(s)"
    print "2. Transfer"
    print "3. View Transaction History"
    print "4. Quit"
    option = raw_input("Enter number: ").strip()
    if option == '1':
        balances = user.get_balance()
        printers.print_balances(balances)
    elif option == '2':
        printers.print_title("TRANSFER FUNDS")
        transaction = Prompter.request_transaction_data()
        try:
            user.make_transaction(transaction)
            print 'Successfully transferred $%s to %s' % (
                transaction.amount, transaction.target_account_id)
        except:
            print 'Invalid target account id'
    elif option == '3':
        transactions = user.get_transactions()
        printers.print_transactions(user, transactions)
    elif option == '4':
        print 'Exiting program'
        break
    else:
        print 'Unrecognized option:', option
