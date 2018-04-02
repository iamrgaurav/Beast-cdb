import uuid
import datetime

import src.models.sim.constants as SimConstants

from src.common.database import Database
from src.common.Utility.Utility import CommonUtility as SimUtility


class Sim:
    def __init__(self, aadhaar_no, sim_no, tsp, lsa, issue_date, status=1, _id=None):
        self._id = uuid.uuid4().hex if _id is None else _id
        self.aadhaar_no = SimUtility.formating_aadhaar(aadhaar_no)
        self.sim_no = SimUtility.formating_phone(sim_no)
        self.tsp = SimUtility.formating_name(tsp)
        self.lsa = SimUtility.formating_name(lsa)
        self.status = status
        self.issue_date = datetime.datetime.strptime(issue_date, "%Y-%m-%d") if isinstance(issue_date,
                                                                                           str) else issue_date

    def json(self):
        return {
            '_id': self._id,
            'sim_no': self.sim_no,
            'aadhaar_no': self.aadhaar_no,
            'tsp': self.tsp,
            'lsa': self.lsa,
            'status':self.status,
            'issue_date': self.issue_date.strftime("%Y-%m-%d")
        }

    def save_to_db(self):
        return Database.update(SimConstants.COLLECTIONS, {'_id': self._id, 'status': 1}, self.json())

    @classmethod
    def get_by_aadhaar(cls, aadhaar_no):
        cluster_data = Database.find(SimConstants.COLLECTIONS, {'aadhaar_no': aadhaar_no,'status':1})
        return [cls(**data) for data in cluster_data if data is not None] if cluster_data is not None else False

    @staticmethod
    def get_sim_count_by_tsp(aadhaar):
        cluster_data = Sim.get_by_aadhaar(aadhaar)
        tsps = []
        for data in cluster_data:
            tsps.append(data.tsp)
        tsps = list(set(tsps))

        sim_counts_by_tsp = {}
        for tsp in tsps:
            count = 0
            for data in cluster_data:
                if tsp == data.tsp:
                    count += 1
            sim_counts_by_tsp[tsp] = count
        return sim_counts_by_tsp

    @classmethod
    def get_all_sim(cls):
        cluster_data = Database.find(SimConstants.COLLECTIONS, {'status':1})
        return [cls(**data) for data in cluster_data if data is not None] if cluster_data is not None else None

    @classmethod
    def get_sim_in_lsa(cls, lsa):
        cluster_data = Database.find(SimConstants.COLLECTIONS, {"lsa": lsa, "status": 1})
        return [cls(**data) for data in cluster_data if data is not None] if cluster_data is not None else None

    @classmethod
    def list_by_count(cls, sim_count):
        sims = cls.get_all_sim()
        aadhaars = []
        for sim in sims:
            aadhaars.append(sim.aadhaar_no)
        aadhaars = list(set(aadhaars))
        data = {}
        for aadhaar in aadhaars:
            count = Database.count(SimConstants.COLLECTIONS, {'aadhaar_no': aadhaar, 'status':1})
            data[aadhaar] = count
        for key in aadhaars:
            if data[key] < int(sim_count):
                del data[key]
        return data

    @classmethod
    def list_by_lsa(cls, lsa):
        sims = cls.get_sim_in_lsa(lsa)
        aadhaars = []
        for sim in sims:
            aadhaars.append(sim.aadhaar_no)
        aadhaars = list(set(aadhaars))
        data = {}
        for aadhaar in aadhaars:
            count = Database.count(SimConstants.COLLECTIONS, {'aadhar_no': aadhaar, 'status':1})
            data[aadhaar] = count

        return data

    @classmethod
    def del_by_tsp(cls, aadhaar, phone):
        return Database.update(SimConstants.COLLECTIONS, {'aadhaar_no': aadhaar, 'sim_no': phone, 'status': 1},{'$set': {'status': 1}})
