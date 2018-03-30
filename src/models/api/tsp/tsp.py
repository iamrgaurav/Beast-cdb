import datetime

import requests

from src.models.sim.sim import Sim
from src.config import fake_aadhaar_url as fau
from src.models.users.user import User


class TSPApi:
    @staticmethod
    def get_sims_by_aadhaar(aadhaar, tsp):
        sims = Sim.get_by_aadhaar(aadhaar)
        return {'aadhaar_no': aadhaar,
                'sim': [{'lsa': sim.lsa,
                         'tsp': sim.tsp,
                         'mobile': sim.sim_no,
                         'issue_date': sim.issue_date.strftime("%Y-%m-%d")
                         } for sim in sims if tsp == sim.tsp] if sims is not None else 0,
                'sims_by_other_tsp': Sim.get_sim_count_by_tsp(aadhaar),
                'Total_Sim': len(sims)
                }

    @staticmethod
    def save_sim(mobile, tsp, issue_date, lsa, aadhaar_no):
        user = User.get_by_aadhaar(aadhaar_no)
        if user:
            return Sim(aadhaar_no, mobile, tsp, lsa, issue_date).save_to_db()
        else:
            data = requests.post(fau, data={'aadhaar_no': aadhaar_no}).json()
            user_info = {
                'aadhaar_no': data['aadhaar'],
                'name': data['name'],
                'dob': data['dob'],
                'address': data['address'],
                'mobile_no': data['phone'],
                'gender': data['gender']}
            if User(**user_info).save_to_db():
                return Sim(aadhaar_no, mobile, tsp, lsa, issue_date).save_to_db()

