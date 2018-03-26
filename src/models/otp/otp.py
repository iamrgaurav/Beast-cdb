import uuid
import random
import datetime
import src.models.otp.constants as OTPConstans

from src.common.database import Database


class OTP:
    def __init__(self, user_id, generation_time = None,otp = None,_id=None):
        self._id=uuid.uuid4().hex if _id is None else _id
        self.otp = str(random.randint(100000, 999999)) if otp is None else otp
        self.generation_time = datetime.datetime.now().strftime("%c") if generation_time is None else generation_time
        self.user_id = user_id

    def json(self):
        return {
            'user_id':self.user_id,
            '_id':self._id,
            'otp':self.otp,
            'generation_time':self.generation_time
        }

    def save_to_db(self):
       return True if Database.update(OTPConstans.COLLECTIONS, {'_id':self._id}, self.json()) else False

    def remove_from_db(self):
        return True if Database.delete(OTPConstans.COLLECTIONS, {'_id': self._id}) else False

    @classmethod
    def get_recent_otp(cls,otp_id):
        data = Database.find_one(OTPConstans.COLLECTIONS, {'_id':otp_id})
        return cls(**data)

