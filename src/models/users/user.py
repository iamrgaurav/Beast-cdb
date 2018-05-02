import uuid

import src.models.users.constants as UserConstants

from src.models.users.sim import Sim
from src.models.otp.otp import OTP

from src.common.database import Database
from src.common.Utility.utils import Utils
from src.common.Utility.Utility import CommonUtility as User_Utility


class User:
    def __init__(self, aadhaar_no, mobile_no, sim_cards = None,_id=None):
        self.aadhaar_no = User_Utility.formating_aadhaar(aadhaar_no)
        self.mobile_no = User_Utility.formating_phone(mobile_no)
        self._id = uuid.uuid4().hex if _id is None else _id
        self.sim_cards = sim_cards if sim_cards is None else [Sim(**sim) for sim in sim_cards]

    @classmethod
    def get_by_id(cls, user_id):
        data = Database.find_one(UserConstants.COLLECTIONS, {'_id': user_id})
        return cls(**data) if data is not None else False

    def json(self):
        return {
            'aadhaar_no': self.aadhaar_no,
            'mobile_no': self.mobile_no,
            'sim_cards': None if self.sim_cards is None else [sim.json() for sim in self.sim_cards],
            '_id': self._id
        }

    def save_to_db(self):
        return Database.update(UserConstants.COLLECTIONS, {'_id': self._id}, self.json())


    def add_sim_card(self, sim_no,tsp,lsa,issue_date):
        sim = Sim(sim_no=sim_no, tsp=tsp, lsa=lsa, issue_date=issue_date)
        self.sim_cards = [sim] if self.sim_cards is None else self.sim_cards.append(sim)
        return self.save_to_db()
     #Database.update(UserConstants.COLLECTIONS,{'_id':self._id},{'$set': {'sim_cards': [sim.json() for sim in self.sim_cards if sim is not None] if self.sim_cards is not None else self.sim_cards }})

    @classmethod
    def list_all_user(cls):
        cluster_data = Database.find(UserConstants.COLLECTIONS, {})
        return [cls(**data) for data in cluster_data if data is not None] if cluster_data is not None else None

    @classmethod
    def get_by_aadhaar(cls, aadhaar_no):
        data = Database.find_one(UserConstants.COLLECTIONS, {'aadhaar_no': aadhaar_no})
        return cls(**data) if data is not None else False


    def send_otp(self):
        otp = OTP(self.aadhaar_no)
        if Utils.send_otp(otp.otp, self.mobile_no):
            otp.save_to_db()
            return otp
        else:
            return False

    def count_sim(self, sent_tsp = None):
        sim_counts = {}
        cluster_tsp = list(set([sim.tsp for sim in self.sim_cards]))
        if sent_tsp in cluster_tsp:
            cluster_tsp.remove(sent_tsp)
        if cluster_tsp is not None:
            for tsp in cluster_tsp:
                count = 0
                for sim in self.sim_cards:
                    if tsp == sim.tsp:
                        count += 1
                sim_counts[tsp] = count
        return sim_counts


    @classmethod
    def list_by_count(cls, count):
        users = User.list_all_user()
        user_list = {}
        for user in users:
            user_sim_count = len(user.sim_cards)
            if user_sim_count>=int(count):
                user_list[user.aadhaar_no]=user_sim_count
        return user_list

    @classmethod
    def list_by_lsa(cls, lsa:str):
        users = User.list_all_user()
        user_list = {}
        for user in users:
            user_sim_count = len(user.sim_cards)
            for sim_card in user.sim_cards:
                if sim_card.lsa.lower() == lsa.lower():
                    user_list[user.aadhaar_no]=user_sim_count
            return user_list