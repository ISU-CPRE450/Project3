from src.prompter import Prompter
from src import printers
from src.user import Banker, Participant
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
            user.__class__ = Participant
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
                    print 'If you are proctoring another game, restart the '\
                          'program to end any games you are proctoring'
            elif option == '2':
                try:
                    user.get_and_print_latest_game_transactions()
                except Exception as e:
                    print 'Error getting latest game transactions:', e.message
            elif option == '3':
                raise KeyboardInterrupt
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
    printers.print_title('PROCTOR GAME')
    print 'Waiting for participants...'
    while len(participants) < 2:
        local_participants = user.get_participants()
        if len(local_participants) > len(participants):
            print 'Participant joined! ID:', \
                local_participants[-1]['user']['account_id']
        elif len(local_participants) == len(participants):
            pass
        else:
            print 'Participant disconnected'
        participants = local_participants
        sleep(1.5)
    winner = None
    try:
        winner = user.get_winner()
    except Exception as e:
        print e.message
        user.resolve_bad_hash()
        return
    participants = user.get_participants()
    print 'Player 1 guess:', participants[0]['random_value']
    print 'Player 2 guess:', participants[1]['random_value']
    loser = None
    if winner['user']['account_id'] == participants[0]['user'][
            'account_id']:
        loser = participants[1]
        print 'Winner: Player 1'
    else:
        loser = participants[0]
        print 'Winner: Player 2'
    user.give_earnings(winner, loser)


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
            amount = Prompter.request_bet_amount()
            try:
                user.join_game(amount)
                enter_game_view()
            except Exception as e:
                print 'Could not join game:', e.message
        elif option == '2':
            print 'attempting to view rounds'
            try:
                user.get_and_print_latest_game()
            except Exception as e:
                print 'Error getting latest game:', e.message
        elif option == '3':
            print 'Exiting program'
            break
        else:
            print 'Unrecognized option:', option


def enter_game_view():
    printers.print_title('PLAY GAME')
    print 'Waiting for other player...'
    while True:
        participant = user.get_other_player()
        if participant:
            try:
                print 'Your number:', user.random_value
                print 'Other player\'s number:', participant['random_value']
                print 'Result:', user.get_result()
            except Exception as e:
                print e.message
            break
        else:
            sleep(1.5)

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
