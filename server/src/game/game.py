from google.appengine.ext import ndb


class Game(ndb.Model):
    banker = ndb.KeyProperty(kind='User', required=True)
    is_active = ndb.BooleanProperty(default=False)
    participants = ndb.KeyProperty(kind='Participant', repeated=True)
    time_created = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def banker_already_proctoring(cls, banker):
        return Game.query(
            Game.banker == banker.key, Game.is_active == True).count() > 0

    @classmethod
    def add(cls, banker):
        g = Game(banker=banker.key, is_active=True)
        g.put()
        return g

    @classmethod
    def get_available_game(cls):
        games = Game.query(Game.is_active == True).fetch()
        for game in games:
            if len(game.participants) != 2:
                return game
        return None

    def add_participant(self, participant):
        if self.has_user(participant):
            raise Exception('This user is already playing this game')
        self.participants.append(participant.key)
        if len(self.participants) == 2:
            self.end()
        else:
            self.put()

    def has_user(self, user):
        for p in ndb.get_multi(self.participants):
            if p.user == user.key:
                return True
        return False

    def end(self):
        self.is_active = False
        self.put()

    def serialize(self):
        d = self._to_dict()
        d['id'] = self.key.id()
        d['banker'] = self.banker.get().serialize()
        d['participants'] = []
        for p in ndb.get_multi(self.participants):
            d['participants'].append(p.serialize())
        d['time_created'] = self.time_created.isoformat()
        return d
