## CPRE 450: Coin Flipping Game

Check it out on Github: https://github.com/ISU-CPRE450/Project3

### Description

This assignment was split into two parts: phase 1 and phase 2.

Phase 1 dealt with interacting with the stellar api. I decided to use
the python sdk to interact with their api.

In phase 2, I created a distributed game that allows two people to
place a bet, flip a coin, and give funds to the winner. See the file
`project_description.pdf` for more info.


### Usage

If you are wanting to check out Phase 1, navigate to the `phase1` folder.
If you are wanting to check out Phase 2, navigate to the `phase2` folder.

In each phase, there are two folders, `client/` and `server/`. The client folder corresponds
to the client (i.e. banker and participant). The server folder contains code
that the server runs.


#### Server Usage

This server was built on Google App Engine (GAE). See
[these docs](https://cloud.google.com/appengine/docs/standard/python/tools/using-local-server)
for information on how to set up a local GAE server. I hard-coded the port number
in the application to 9088. You can run the server on that port, or you can
change the constant named `SERVER_URL` in `client/src/user.py` to specify
your desired port.


#### Client Usage

To use the client run the following commands (for unix)

```
cd client
source /env/bin/activate
pip install requirements.txt
python main.py
```

This will start the client program. You cannot do much in the client without
the server. See server usage below to start the server. Once the server is
running, you will be able to create an account or login.


### Technical details

I used python's sha224 (from the hashlib module) for perform all of my hashing.

The protocol used  for coin flipping goes as follows:

1. Generate random integer.

2. Hash the integer and send it to server.

3. Once both parties have sent their values to the server, check that the
values they say they chose are equal to the hash value originally sent.

The way that users could try to attack this system is by changing their value
based on the value of the other person. Adding one or subtracting one from the
original value would result in a different outcome of the game. In my
implementation, I require the user to send their hashed value to the server
before they even join a game. That way, the user will receive no information on
anyone else before the game starts. Also, we check this random value after the
game has been played and ensure it matches what was originally sent to the
server.


### Design

I decided to solve this by creating a client that supports both bankers and
participants. I created a server that will store information such as users and
games. The server pretty much just acts as a database. Users will send requests
to this server to join games. The server will store all transaction and game
history.

The workflow of the game is as follows:

1. Banker chooses to proctor a game
2. A new game becomes available
3. Banker waits for participants to join game
4. Participant attempts to join game
5. Participant is required to choose bet amount.
6. Random value is generated, hashed, and sent to server along with bet amount.
7. Bet amount is transferred to banker
8. Participant waits for another participant to join
9. Repeat steps 3-5 to add new participant
10. Banker detects two participants have joined
11. Banker and participants view who winner is.
12. Banker sends 95% of earnings to winner.
13. Round is over
