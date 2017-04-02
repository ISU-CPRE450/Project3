from src.prompter import Prompter
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
    title = "=" * 10 + " %s Home Screen " + "=" * 10
    title = title % user.email
    print "1. Check Balance"
    print "2. Transfer"
    print "3. View Transaction History"
    print "4. Quit"
    option = raw_input("Enter number: ")
    if option == '1':
        print 'checking balance'
    if option == '2':
        print 'transferring funds'
    if option == '3':
        print 'viewing transaction history'
    elif option == '4':
        print 'Exiting program'
        break
    else:
        print 'Unrecognized option:', option
