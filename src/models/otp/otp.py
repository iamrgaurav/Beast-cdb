import uuid
import random
import datetime
import src.models.otp.constants as OTPConstans

from src.common.database import Database


class OTP:
    def __init__(self, aadhaar_no, generation_time=None, otp=None,_id=None):
        self._id=uuid.uuid4().hex if _id is None else _id
        self.otp = str(random.randint(100000, 999999)) if otp is None else otp
        self.generation_time = datetime.datetime.utcnow()\
            if generation_time is None\
            else datetime.datetime.strptime(generation_time,"%c")
        self.aadhaar_no = aadhaar_no

    def json(self):
        return {
            'aadhaar_no': self.aadhaar_no,
            '_id': self._id,
            'otp': self.otp,
            'generation_time': self.generation_time.strftime("%c")
        }

    def save_to_db(self):
       return True if Database.update(OTPConstans.COLLECTIONS, {'_id':self._id}, self.json()) else False

    def remove_from_db(self):
        return True if Database.delete(OTPConstans.COLLECTIONS, {'_id': self._id}) else False

    @classmethod
    def get_recent_otp(cls, otp_id):
        data = Database.find_one(OTPConstans.COLLECTIONS, {'_id': otp_id})
        return cls(**data)

