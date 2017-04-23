## CPRE 450: Coin Flipping Game

### Description

In this assignment, we created a distributed game that allows two people to
place a bet, flip a coin, and give funds to the winner. See the file
`project_description.pdf` for more info.


### Usage

There are two folders, `client/` and `server/`. The client folder corresponds
to the client (i.e. banker and participant). The server folder contains code
that the server runs.

#### Client Usage

To use the client run the following commands (for unix)

```
cd client
source /env/bin/activate
python main.py
```

This will start the client program. You cannot do much in the client without
the server. See server usage below to start the server. Once the server is
running, you will be able to create an account or login.

#### Server Usage

This server was built on Google App Engine (GAE). See
[these docs](https://cloud.google.com/appengine/docs/standard/python/tools/using-local-server)
for information on how to set up a local GAE server. I hard-coded the port number
in the application to 9088. You can run the server on that port, or you can
change the constant named `SERVER_URL` in `client/src/user.py` to specify
your desired port.
