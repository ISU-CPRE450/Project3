from google.appengine.ext import ndb


class Game(ndb.Model):
    banker = ndb.KeyProperty(kind='User', required=True)
    is_active = ndb.BooleanProperty(default=False)
    participants = ndb.KeyProperty(kind='Participant', repeated=True)

    @classmethod
    def banker_already_proctoring(cls, banker):
        return Game.query(
            Game.banker == banker.key, Game.is_active == True).count() > 0

    @classmethod
    def add(cls, banker):
        g = Game(banker=banker.key, is_active=True)
        g.put()
        return g

    def end(self):
        self.is_active = False
        self.put()

    def serialize(self):
        d = self._to_dict()
        d['id'] = self.key.id()
        d['banker'] = self.banker.get().serialize()
        d['participants'] = []
        for p in self.participants:
            d['participants'].append(p.serialize())
        return d
