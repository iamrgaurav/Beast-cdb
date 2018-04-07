import requests

from src.config import fake_aadhaar_url as fau
from src.models.users.user import User


class TSPApi:
    @staticmethod
    def get_sims_by_aadhaar(aadhaar:str, tsp:str):
        user = User.get_by_aadhaar(aadhaar)
        return {'aadhaar_no': user.aadhaar_no,
                'sim_cards_by_your_tsp': [sim_card.json() for sim_card in user.sim_cards if sim_card.tsp == tsp],
                'sim_cards_by_other_tsp': [user.count_sim(tsp)]
                }

    @staticmethod
    def save_sim(mobile, tsp, issue_date, lsa, aadhaar_no):
        user = User.get_by_aadhaar(aadhaar_no)
        if user:
            return user.add_sim_card(mobile,tsp,lsa,issue_date)
        else:
            data = requests.post(fau, data={'aadhaar_no': aadhaar_no}).json()
            if data is not None:
                user_info = {
                    'aadhaar_no': data['aadhaar'],
                    'mobile_no': data['phone']}
                user = User(**user_info)
                if user.add_sim_card(mobile, tsp, lsa, issue_date):
                    return {'msg':'User create Successfully'}, 200
                return {'msg':'There is no record of adhaar {}'.format(aadhaar_no)},400
            return {'msg':'Some unusual Error'}, 400

    @classmethod
    def del_user(cls, aadhaar, phone):
        pass