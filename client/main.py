from src.prompter import Prompter
from src import printers
from src.user import Banker
from time import sleep


def play_as_banker_or_participant():
    while True:
        printers.print_title("SELECT ROLE")
        print 'Are you a banker or participant?'
        print '1. Banker'
        print '2. Participant'
        option = raw_input('Enter number: ').strip()
        if option == '1':
            user.__class__ = Banker
            play_as_banker()
            break
        elif option == '2':
            play_as_participant()
            break
        else:
            print 'Unrecognized option:', option


def play_as_banker():
    try:
        while True:
            printers.print_title(user.email + ' Home Screen (Banker)')
            print "1. Proctor game"
            print "2. View history"
            print "3. Quit"
            option = raw_input("Enter number: ").strip()
            if option == '1':
                try:
                    user.proctor_new_game()
                    print 'Started proctoring new game!'
                    enter_proctor_view()
                except Exception as e:
                    print 'Error:', e.message
            elif option == '2':
                print 'attempting to view history'
            elif option == '3':
                try:
                    user.disconnect_from_game()
                except Exception as e:
                    print 'Error:', e.message
                print 'Exiting program'
                break
            else:
                print 'Unrecognized option:', option
    except Exception as e:
        print 'Error:', e
        print 'Exiting program'
    except KeyboardInterrupt as e:
        print ''
        print 'Exiting program'
    finally:
        user.disconnect_from_game()


def enter_proctor_view():
    participants = []
    while True:
        printers.print_title('PROCTOR GAME')
        if len(participants) == 0:
            print 'Waiting for participants...'
        while len(participants) < 2:
            local_participants = user.get_participants()
            if len(local_participants) > len(participants):
                print 'Participant joined! ID:', \
                    local_participants[-1].account_id
            elif len(local_participants) == len(participants):
                pass
            else:
                print 'Participant disconnected'
            participants = local_participants
            sleep(1.5)


def play_as_participant():
    while True:
        printers.print_title(user.email + ' Home Screen (Participant)')
        '''
        print "1. Check Balance(s)"
        print "2. Transfer"
        print "3. View Transaction History"
        print "4. Quit"
        '''
        print "1. Join game"
        print "2. View results from previous round"
        print "3. Quit"
        option = raw_input("Enter number: ").strip()
        if option == '1':
            print 'attempting to join game'
        elif option == '2':
            print 'attempting to view rounds'
            '''
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
            '''
        elif option == '3':
            print 'Exiting program'
            break
        else:
            print 'Unrecognized option:', option

# START GAME

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
        play_as_banker_or_participant()
    except Exception as e:
        print "Failure:", e.message
