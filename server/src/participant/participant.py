from google.appengine.ext import ndb


class Participant(ndb.Model):
    bet_amount = ndb.FloatProperty(required=True)
    hash_value = ndb.IntegerProperty(required=True)
    user = ndb.KeyProperty(kind='User', required=True)

    @classmethod
    def create(cls, user, amount, hash_value):
        participant = cls(
            user=user,
            bet_amount=amount,
            hash_value=hash_value
        )
        participant.put()
        return participant

    def serialize(self):
        d = self._to_dict()
        d['user'] = self.user.get().serialize()
        return d
