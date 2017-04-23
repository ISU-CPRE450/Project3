from google.appengine.ext import ndb


class Participant(ndb.Model):
    bet_amount = ndb.FloatProperty()
    hash_value = ndb.StringProperty()
    user = ndb.KeyProperty(kind='User', required=True)
    random_value = ndb.IntegerProperty()
    time_created = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def create(cls, user=None, amount=None, hash_value=None,
               random_value=None):
        participant = cls(
            user=user,
            bet_amount=amount,
            hash_value=hash_value,
            random_value=random_value
        )
        participant.put()
        return participant

    def serialize(self):
        d = self._to_dict()
        d['user'] = self.user.get().serialize()
        d['time_created'] = self.time_created.isoformat()
        return d
