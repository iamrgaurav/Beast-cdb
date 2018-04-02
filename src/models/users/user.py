import uuid

import src.models.users.constants as UserConstants

from src.models.sim.sim import Sim
from src.models.otp.otp import OTP

from src.common.database import Database
from src.common.Utility.utils import Utils
from src.common.Utility.Utility import CommonUtility as User_Utility


class User:
    def __init__(self, aadhaar_no, name, address, mobile_no, _id=None):
        self.aadhaar_no = User_Utility.formating_aadhaar(aadhaar_no)
        self.name = User_Utility.formating_name(name)
        self.address = address
        self.mobile_no = User_Utility.formating_phone(mobile_no)
        self._id = uuid.uuid4().hex if _id is None else _id

    @classmethod
    def get_by_id(cls, user_id):
        data = Database.find_one(UserConstants.COLLECTIONS, {'_id': user_id})
        return cls(**data) if data is not None else False

    def json(self):
        return {
            'aadhaar_no': self.aadhaar_no,
            'name': self.name,
            'address': self.address,
            'mobile_no': self.mobile_no,
            '_id': self._id
        }

    def save_to_db(self):
        return Database.update(UserConstants.COLLECTIONS, {'_id': self._id}, self.json())

    @classmethod
    def list_all_user(cls):
        cluster_data = Database.find(UserConstants.COLLECTIONS, {})
        return [cls(**data) for data in cluster_data if data is not None] if cluster_data is not None else None

    @classmethod
    def get_by_aadhaar(cls, aadhaar_no):
        data = Database.find_one(UserConstants.COLLECTIONS, {'aadhaar_no': aadhaar_no})
        return cls(**data) if data is not None else False

    def get_sim_details(self):
        user_sims = Sim.get_by_aadhaar(self.aadhaar_no)
        return user_sims

    def send_otp(self):
        otp = OTP(self.aadhaar_no)
        if Utils.send_otp(otp.otp, self.mobile_no):
            otp.save_to_db()
            return otp
        else:
            return False
